from flask import *
import hashlib
import json
import random
from shortuuid import uuid
import os
app = Flask(__name__)

app.config["SECRET_KEY"] = "SDFL:JSDFLKJSDFlJKSDFlkj"
with open("db/users.json") as fp:
    user_data = json.load(fp)
with open("db/listings.json") as fp:
    listings = json.load(fp)

# region helpers


def hasher(text) -> str: h = hashlib.md5(text.encode()); return h.hexdigest()


def dumpJson():
    with open("db/users.json", "w+") as fp:
        json.dump(user_data, fp, indent=4)
    with open("db/listings.json", "w+") as fp:
        json.dump(listings, fp, indent=4)

# endregion


# region AUTH
@app.route('/sign-up', methods=['post', 'get'])
def sign_up():
    global user_data
    name = request.form['name']
    pw = request.form['pw']
    phone = request.form['pn']

    if name in user_data.keys():
        flash("Username taken", category="error")
        return redirect("/")
    if len(name) > 20:
        flash("Character maximum is 20.", category="error")
        return redirect("/")
    else:
        user_data[name] = {}
        user_data[name]['pw'] = hasher(pw)
        user_data[name]['phone'] = phone
        user_data[name]["listings"] = []
        user_data[name]["favs"] = []

        dumpJson()

        cookie = make_response(redirect("/"))
        cookie.set_cookie('name', name)
        cookie.set_cookie('pw', pw)
        cookie.set_cookie('phone', phone)
        return cookie


@app.route('/login', methods=['post', 'get'])
def login():
    global user_data
    name = request.form['name']
    pw = request.form['pw']
    if name in user_data.keys():
        if user_data[name]['pw'] == hasher(pw):
            cookie = make_response(redirect("/"))
            cookie.set_cookie('name', name)
            cookie.set_cookie('pw', pw)
            flash("Logged in!", category="success")
            return cookie
        else:
            flash("Username or password incorrect.", category="error")
            return redirect("/")
    else:
        flash("Username or password incorrect.", category="error")
        return redirect("/")


@app.route('/logout')
def logout():
    cookie = make_response(redirect("/"))
    cookie.delete_cookie('name')
    cookie.delete_cookie('pw')
    flash("Logged out!", category="success")
    return cookie


# endregion


# region index
@app.route('/')
def index():
    global user_data
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if user_data[cookie_name]['pw'] == hasher(cookie_pw):
                return render_template("index.html", logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            else:
                return render_template("index.html", logged=False, r=random.randint(0, 10000))
        except KeyError:
            return render_template("index.html", logged=False, r=random.randint(0, 10000))
    else:
        return render_template("index.html", logged=False, r=random.randint(0, 10000))


@app.route('/new-listing')
def new_listing():
    cookie_name = request.cookies.get("name")
    cookie_pw = request.cookies.get("pw")
    if (
        not cookie_name
        or not cookie_pw
        or user_data[cookie_name]["pw"] != hasher(cookie_pw)
    ):
        flash("Please login first.", category="error")
        return redirect("/")

    return render_template("create.html", logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))


@app.route('/add-listing', methods=['post'])
def add_listing():

    title = request.form.get("title")
    description = request.form.get("description")
    condition = request.form.get("condition")
    price = request.form.get("price")
    images = request.files
    listingId = uuid()
    date = request.form.get("date")
    os.mkdir(f"./static/listing_images/{listingId}")
    category = request.form.get("category")
    imageTypes = []
    for i in range(len(images)):
        image = images[f"image{i+1}"]
        imageExtension = os.path.splitext(image.filename)[1]
        imageTypes.append(imageExtension[1:])
        image.save(f"./static/listing_images/{listingId}/{i}{imageExtension}")


    listings[listingId] = {
        "title": title,
        "description": description,
        "condition": condition,
        "price": price,
        "id": listingId,
        "imageType": imageTypes,
        "owner": request.cookies.get("name"),
        "category": category,
        "date": date
        # "images": images,
    }
    user_data[request.cookies.get("name")]["listings"].append(listingId)
    dumpJson()

    return listingId


@app.route('/search', methods=['POST'])
def search():

    text = request.form.get('text')
    tl = text.lower()
    res = []
    for listing in listings:
        listingl = listings[listing]["title"].lower()
        if listingl in tl or tl.endswith(listingl) or listingl.endswith(tl) or tl.startswith(listingl) or listingl.startswith(tl) or tl == listingl or tl in listingl:
            res.append(listings[listing])
    
    return jsonify({"res":res})


@app.route('/listing/<listingId>')
def lising(listingId):
    if listingId not in listings:
        flash("Listing not found.", category="error")
        return redirect("/")
    
    cookie_name = request.cookies.get("name")
    cookie_pw = request.cookies.get("pw")
    if (
    not cookie_name
    or not cookie_pw
    or user_data[cookie_name]["pw"] != hasher(cookie_pw)
    ):
        return render_template('listing.html', listing=listings[listingId],  logged=False, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))


    return render_template('listing.html', listing=listings[listingId],  logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            

@app.route('/user/<targetName>')
def user(targetName):
    if targetName not in user_data.keys() or not request.cookies.get("name") or not request.cookies.get("pw") or user_data[request.cookies.get("name")]["pw"] != hasher(request.cookies.get("pw")):
        flash("User not found", category="error")
        return redirect('/')
    phone = user_data[targetName]["phone"]
    targetListings = user_data[targetName]["listings"]
    listingsRes = [listings[l] for l in targetListings]

    return render_template("profile.html", phone=phone, listings=listingsRes,targetName=targetName,logged=True, username=request.cookies.get("name"), pw=request.cookies.get("pw"), r=random.randint(0, 10000))



@app.route('/add-to-fav_listingId=<listingId>')
def addToFav(listingId):
    username = request.cookies.get('username')
    pw = request.cookies.get('pw')

    if hasher(pw) != user_data[username]["pw"]:
        return jsonify({"res": "Wrong password"})

    if listingId in listings.keys() and listingId not in user_data[username]["favs"]: 
        user_data[username]["favs"].append(listingId)
        dumpJson()
        return jsonify({"res": "success"})
    else:
        return jsonify({"res":"listing not found"})

@app.route('/remove-from-fav_listingId=<listingId>')
def removeFromFav(listingId):
    username = request.cookies.get('username')
    pw = request.cookies.get('pw')

    if hasher(pw) != user_data[username]["pw"]:
        return jsonify({"res": "Wrong password"})

    if listingId in listings and listingId in user_data[username]["favs"]: 
        user_data[username]["favs"].remove(listingId)
        dumpJson()
        return jsonify({"res": "success"})
    else:
        return jsonify({"res":"listing not found"})


@app.route('/get-my-favs')
def getMyFavs():
    pw = request.cookies.get('pw')
    username = request.cookies.get('username')
    if hasher(pw) == user_data[username]["pw"]:
        return jsonify({"res": user_data[username]["favs"]})
    else:
        return jsonify({"res": "wrong password"}) 


@app.route('/favorites')
def favorites():
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if user_data[cookie_name]['pw'] == hasher(cookie_pw):
                favListings = []
                for listing in user_data[cookie_name]['favs']:
                    favListings.append(listings[listing])
                

                return render_template("favorites.html", favListings=favListings,logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            else:
                flash("Please login first", category="error")
                return redirect('/')
        except KeyError:
                flash("Please login first", category="error")
                return redirect('/')
    else:
                flash("Please login first", category="error")
                return redirect('/') 

@app.route("/search-with-category_cat=<category>")
def search_with_category(category):
    res = []
    for listing in listings:
        if listings[listing]["category"] == category:
            res.append(listings[listing])
    return jsonify({"res": res})


@app.route('/flash=<flashMessage>_url=<url>')
def customFlash(flashMessage, url):
    print(url)
    flash(flashMessage)
    url = "/" if url == "EMPTY" else "/" + url.replace("SLASH", "/")

    return redirect(url)

    


    


app.run(host='localhost', port=8000, debug=True)
