# coding=utf8
import datetime
from flask import *
import hashlib
import json
import random
import requests
from shortuuid import uuid
import os
import shutil
from countryinfo import CountryInfo
app = Flask(__name__)

app.config["SECRET_KEY"] = "SDFL:JSDFLKJSDFlJKSDFlkj"
with open("db/users.json") as fp:
    user_data = json.load(fp)
with open("db/listings.json") as fp:
    listings = json.load(fp)
with open("db/reports.json") as fp:
    reports = json.load(fp)
# region helpers

countries = {'Ascension Island': '🇦🇨', 'Andorra': '🇦🇩', 'United Arab Emirates': '🇦🇪', 'Afghanistan': '🇦🇫', 'Antigua & Barbuda': '🇦🇬', 'Anguilla': '🇦🇮', 'Albania': '🇦🇱', 'Armenia': '🇦🇲', 'Angola': '🇦🇴', 'Antarctica': '🇦🇶', 'Argentina': '🇦🇷', 'American Samoa': '🇦🇸', 'Austria': '🇦🇹', 'Australia': '🇦🇺', 'Aruba': '🇦🇼', 'Åland Islands': '🇦🇽', 'Azerbaijan': '🇦🇿', 'Bosnia & Herzegovina': '🇧🇦', 'Barbados': '🇧🇧', 'Bangladesh': '🇧🇩', 'Belgium': '🇧🇪', 'Burkina Faso': '🇧🇫', 'Bulgaria': '🇧🇬', 'Bahrain': '🇧🇭', 'Burundi': '🇧🇮', 'Benin': '🇧🇯', 'St. Barthélemy': '🇧🇱', 'Bermuda': '🇧🇲', 'Brunei': '🇧🇳', 'Bolivia': '🇧🇴', 'Caribbean Netherlands': '🇧🇶', 'Brazil': '🇧🇷', 'Bahamas': '🇧🇸', 'Bhutan': '🇧🇹', 'Bouvet Island': '🇧🇻', 'Botswana': '🇧🇼', 'Belarus': '🇧🇾', 'Belize': '🇧🇿', 'Canada': '🇨🇦', 'Cocos (Keeling) Islands': '🇨🇨', 'Congo - Kinshasa': '🇨🇩', 'Central African Republic': '🇨🇫', 'Congo - Brazzaville': '🇨🇬', 'Switzerland': '🇨🇭', 'Côte d’Ivoire': '🇨🇮', 'Cook Islands': '🇨🇰', 'Chile': '🇨🇱', 'Cameroon': '🇨🇲', 'China': '🇨🇳', 'Colombia': '🇨🇴', 'Clipperton Island': '🇨🇵', 'Costa Rica': '🇨🇷', 'Cuba': '🇨🇺', 'Cape Verde': '🇨🇻', 'Curaçao': '🇨🇼', 'Christmas Island': '🇨🇽', 'Cyprus': '🇨🇾', 'Czechia': '🇨🇿', 'Germany': '🇩🇪', 'Diego Garcia': '🇩🇬', 'Djibouti': '🇩🇯', 'Denmark': '🇩🇰', 'Dominica': '🇩🇲', 'Dominican Republic': '🇩🇴', 'Algeria': '🇩🇿', 'Ceuta & Melilla': '🇪🇦', 'Ecuador': '🇪🇨', 'Estonia': '🇪🇪', 'Egypt': '🇪🇬', 'Western Sahara': '🇪🇭', 'Eritrea': '🇪🇷', 'Spain': '🇪🇸', 'Ethiopia': '🇪🇹', 'European Union': '🇪🇺', 'Finland': '🇫🇮', 'Fiji': '🇫🇯', 'Falkland Islands': '🇫🇰', 'Micronesia': '🇫🇲', 'Faroe Islands': '🇫🇴', 'France': '🇫🇷', 'Gabon': '🇬🇦', 'United Kingdom': '🇬🇧', 'Grenada': '🇬🇩', 'Georgia': '🇬🇪', 'French Guiana': '🇬🇫', 'Guernsey': '🇬🇬', 'Ghana': '🇬🇭', 'Gibraltar': '🇬🇮', 'Greenland': '🇬🇱', 'Gambia': '🇬🇲', 'Guinea': '🇬🇳', 'Guadeloupe': '🇬🇵', 'Equatorial Guinea': '🇬🇶', 'Greece': '🇬🇷', 'South Georgia & South Sandwich Islands': '🇬🇸', 'Guatemala': '🇬🇹', 'Guam': '🇬🇺', 'Guinea-Bissau': '🇬🇼', 'Guyana': '🇬🇾', 'Hong Kong SAR China': '🇭🇰', 'Heard & McDonald Islands': '🇭🇲', 'Honduras': '🇭🇳', 'Croatia': '🇭🇷', 'Haiti': '🇭🇹', 'Hungary': '🇭🇺', 'Canary Islands': '🇮🇨', 'Indonesia': '🇮🇩', 'Ireland': '🇮🇪', 'Israel': '🇮🇱', 'Isle of Man': '🇮🇲', 'India': '🇮🇳', 'British Indian Ocean Territory': '🇮🇴', 'Iraq': '🇮🇶', 'Iran': '🇮🇷', 'Iceland': '🇮🇸', 'Italy': '🇮🇹', 'Jersey': '🇯🇪', 'Jamaica': '🇯🇲', 'Jordan': '🇯🇴', 'Japan': '🇯🇵', 'Kenya': '🇰🇪', 'Kyrgyzstan': '🇰🇬', 'Cambodia': '🇰🇭', 'Kiribati': '🇰🇮', 'Comoros': '🇰🇲', 'St. Kitts & Nevis': '🇰🇳', 'North Korea': '🇰🇵', 'South Korea': '🇰🇷', 'Kuwait': '🇰🇼', 'Cayman Islands': '🇰🇾', 'Kazakhstan': '🇰🇿', 'Laos': '🇱🇦', 'Lebanon': '🇱🇧', 'St. Lucia': '🇱🇨', 'Liechtenstein': '🇱🇮', 'Sri Lanka': '🇱🇰', 'Liberia': '🇱🇷', 'Lesotho': '🇱🇸', 'Lithuania': '🇱🇹', 'Luxembourg': '🇱🇺', 'Latvia': '🇱🇻', 'Libya': '🇱🇾', 'Morocco': '🇲🇦', 'Monaco': '🇲🇨', 'Moldova': '🇲🇩', 'Montenegro': '🇲🇪', 'St. Martin': '🇲🇫', 'Madagascar': '🇲🇬', 'Marshall Islands': '🇲🇭', 'North Macedonia': '🇲🇰', 'Mali': '🇲🇱', 'Myanmar (Burma)': '🇲🇲', 'Mongolia': '🇲🇳', 'Macao Sar China': '🇲🇴', 'Northern Mariana Islands': '🇲🇵', 'Martinique': '🇲🇶', 'Mauritania': '🇲🇷', 'Montserrat': '🇲🇸', 'Malta': '🇲🇹', 'Mauritius': '🇲🇺', 'Maldives': '🇲🇻', 'Malawi': '🇲🇼', 'Mexico': '🇲🇽', 'Malaysia': '🇲🇾', 'Mozambique': '🇲🇿', 'Namibia': '🇳🇦', 'New Caledonia': '🇳🇨', 'Niger': '🇳🇪', 'Norfolk Island': '🇳🇫', 'Nigeria': '🇳🇬', 'Nicaragua': '🇳🇮', 'Netherlands': '🇳🇱', 'Norway': '🇳🇴', 'Nepal': '🇳🇵', 'Nauru': '🇳🇷', 'Niue': '🇳🇺', 'New Zealand': '🇳🇿', 'Oman': '🇴🇲', 'Panama': '🇵🇦', 'Peru': '🇵🇪', 'French Polynesia': '🇵🇫', 'Papua New Guinea': '🇵🇬', 'Philippines': '🇵🇭', 'Pakistan': '🇵🇰', 'Poland': '🇵🇱', 'St. Pierre & Miquelon': '🇵🇲', 'Pitcairn Islands': '🇵🇳', 'Puerto Rico': '🇵🇷', 'Palestinian Territories': '🇵🇸', 'Portugal': '🇵🇹', 'Palau': '🇵🇼', 'Paraguay': '🇵🇾', 'Qatar': '🇶🇦', 'Réunion': '🇷🇪', 'Romania': '🇷🇴', 'Serbia': '🇷🇸', 'Russia': '🇷🇺', 'Rwanda': '🇷🇼', 'Saudi Arabia': '🇸🇦', 'Solomon Islands': '🇸🇧', 'Seychelles': '🇸🇨', 'Sudan': '🇸🇩', 'Sweden': '🇸🇪', 'Singapore': '🇸🇬', 'St. Helena': '🇸🇭', 'Slovenia': '🇸🇮', 'Svalbard & Jan Mayen': '🇸🇯', 'Slovakia': '🇸🇰', 'Sierra Leone': '🇸🇱', 'San Marino': '🇸🇲', 'Senegal': '🇸🇳', 'Somalia': '🇸🇴', 'Suriname': '🇸🇷', 'South Sudan': '🇸🇸', 'São Tomé & Príncipe': '🇸🇹', 'El Salvador': '🇸🇻', 'Sint Maarten': '🇸🇽', 'Syria': '🇸🇾', 'Eswatini': '🇸🇿', 'Tristan Da Cunha': '🇹🇦', 'Turks & Caicos Islands': '🇹🇨', 'Chad': '🇹🇩', 'French Southern Territories': '🇹🇫', 'Togo': '🇹🇬', 'Thailand': '🇹🇭', 'Tajikistan': '🇹🇯', 'Tokelau': '🇹🇰', 'Timor-Leste': '🇹🇱', 'Turkmenistan': '🇹🇲', 'Tunisia': '🇹🇳', 'Tonga': '🇹🇴', 'Turkey': '🇹🇷', 'Trinidad & Tobago': '🇹🇹', 'Tuvalu': '🇹🇻', 'Taiwan': '🇹🇼', 'Tanzania': '🇹🇿', 'Ukraine': '🇺🇦', 'Uganda': '🇺🇬', 'U.S. Outlying Islands': '🇺🇲', 'United Nations': '🇺🇳', 'United States': '🇺🇸', 'Uruguay': '🇺🇾', 'Uzbekistan': '🇺🇿', 'Vatican City': '🇻🇦', 'St. Vincent & Grenadines': '🇻🇨', 'Venezuela': '🇻🇪', 'British Virgin Islands': '🇻🇬', 'U.S. Virgin Islands': '🇻🇮', 'Vietnam': '🇻🇳', 'Vanuatu': '🇻🇺', 'Wallis & Futuna': '🇼🇫', 'Samoa': '🇼🇸', 'Kosovo': '🇽🇰', 'Yemen': '🇾🇪', 'Mayotte': '🇾🇹', 'South Africa': '🇿🇦', 'Zambia': '🇿🇲', 'Zimbabwe': '🇿🇼'}
def hasher(text) -> str: h = hashlib.md5(text.encode()); return h.hexdigest()


def dumpJson():
    with open("db/users.json", "w+") as fp:
        json.dump(user_data, fp, indent=4)
    with open("db/listings.json", "w+") as fp:
        json.dump(listings, fp, indent=4)
    with open("db/reports.json", "w+") as fp:
        json.dump(reports, fp, indent=4)
# endregion


# region AUTH
@app.route('/sign-up', methods=['post', 'get'])
def sign_up():
    global user_data
    name = request.form['name']
    pw = request.form['pw']
    phone = request.form['pn']
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    if ip == "127.0.0.1" :
        ip = "45.240.198.19"
    country = requests.get("http://ip-api.com/json/" + ip).json()["country"]
    try:
        phone += f" ({countries[country]})"
    except:
        pass
    if len(phone) == 0 or phone == "" or phone.replace(" ", "") == "" or len(phone) > 15 + 5: # we add 5 for the extra chars from the flag
        flash("Invalid phone number.", category="error")
        return redirect('/')


    # for user in user_data:
    #     if user_data[user]["phone"] == phone:
    #         flash("Phone number already in use.", category="error")
    #         return redirect('/')
    #? RE ADD THIS AFTER NUMBER VERIFYING
    
    for l in phone:
        if l.isalpha():
            flash("Phone number cannot contain letters.", category="error")
            return redirect('/')
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
        user_data[name]["chats"] = {}
        '''
        chats = 
            {
                "user1": [["user1", "lol"], ["user1", "haha"], ["karim", "bruh"]],
                "tester" : [["tester", "hello"], ["karim", "whats up"]]
            }
        
        
        '''
        # user_data[name]["pfp"] = "https://api-private.atlassian.com/users/aa7543e682dff486562017fe2fedc6c0/avatar"
        

        dumpJson()

        cookie = make_response(redirect("/"))
        cookie.set_cookie('name', name)
        cookie.set_cookie('pw', pw)
        cookie.set_cookie('phone', phone)
        flash("Account created, Welcome to Sellio!")
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

def getLatestListings():
    
    if len(list(listings.keys())) >= 15:
        res = [listings[list(listings.keys())[-i]] for i in range(15)]
    else:
        res = [listings[list(listings.keys())[-i]] for i in range(len(listings.keys()))]

    return res
@app.route('/')
def index():
    global user_data
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if user_data[cookie_name]['pw'] == hasher(cookie_pw):
                return render_template("index.html", logged=True, latestListings=getLatestListings(),username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            else:
                return render_template("index.html", latestListings=getLatestListings(), logged=False, r=random.randint(0, 10000))
        except KeyError:
            return render_template("index.html",  latestListings=getLatestListings() ,logged=False, r=random.randint(0, 10000))
    else:
        return render_template("index.html", latestListings=getLatestListings(), logged=False, r=random.randint(0, 10000))


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

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    if ip == "127.0.0.1" :
        ip = "45.240.198.19"
    
    country = requests.get("http://ip-api.com/json/" + ip).json()["country"]
    currency = CountryInfo(country).currencies()[0]
    return render_template("create.html", logged=True, currency=currency,username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))


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

    if price.isalpha():
        
        return "error uploading"
    for i in range(len(images)):
        image = images[f"image{i+1}"]
        imageExtension = os.path.splitext(image.filename)[1]
        imageTypes.append(imageExtension[1:])
        image.save(f"./static/listing_images/{listingId}/{i}{imageExtension}")

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    if ip == "127.0.0.1" :
        ip = "45.240.198.19"
    
    country = requests.get("http://ip-api.com/json/" + ip).json()["country"]
    currency = CountryInfo(country).currencies()[0]
    listings[listingId] = {
        "title": title,
        "description": description,
        "condition": condition,
        "price": price,
        "currency": currency,
        "id": listingId,
        "imageType": imageTypes,
        "owner": request.cookies.get("name"),
        "category": category,
        "date": date
        # "images": images,
    }
    user_data[request.cookies.get("name")]["listings"].append(listingId)
    reports[listingId] = []
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
        return render_template('listing.html', listing=listings[listingId], targetPhone=user_data[listings[listingId]["owner"]]["phone"], logged=False, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))


    return render_template('listing.html', listing=listings[listingId], targetPhone=user_data[listings[listingId]["owner"]]["phone"] , logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            

@app.route('/user/<targetName>')
def user(targetName):
    if targetName not in user_data.keys():
        flash("User not found", category="error")
        return redirect('/')
    phone = user_data[targetName]["phone"]
    targetListings = user_data[targetName]["listings"]
    listingsRes = [listings[l] for l in targetListings]
    if not request.cookies.get("name") or not request.cookies.get("pw"):
        return render_template("profile.html", phone=phone, listings=listingsRes,targetName=targetName,logged=False, r=random.randint(0, 10000))

    return render_template("profile.html", phone=phone, listings=listingsRes,targetName=targetName,logged=True, username=request.cookies.get("name"), pw=request.cookies.get("pw"), r=random.randint(0, 10000))



@app.route('/add-to-fav_listingId=<listingId>')
def addToFav(listingId):
    username = request.cookies.get('name')
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
    username = request.cookies.get('name')
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
    username = request.cookies.get('name')
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



@app.route('/remove-listing_id=<id>')
def removeListing(id):
    pw = request.cookies.get('pw')
    username = request.cookies.get('name')
    print(pw, username)
    if hasher(pw) != user_data[username]["pw"]:
        return jsonify({"res":"wrong password"})
    if id not in listings.keys():
        return jsonify({"res":"listing not found"})

    for _ in range(len(listings[id]["imageType"])):
        shutil.rmtree("./static/listing_images/" + id )
    user_data[username]["listings"].remove(id)
    del listings[id]
    for user in user_data:
        if id in user_data[user]["favs"]:
            user_data[user]["favs"].remove(id)
    dumpJson()
    return jsonify({"res":"success"})



@app.route('/change-pfp', methods=['POST'])
def changePfp():
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')
    if hasher(pw) == user_data[username]["pw"]:
        newPfp = request.files["image"]
        newPfp.save("static/pfps/" +username + os.path.splitext(newPfp.filename)[1])
        # user_data[username]["pfp"] = "/static/pfp/" + username + os.path.splitext(newPfp.filename)[1]
        return "success"
    else:
        return "wrong password"



@app.route('/chats')
def chats():
    username = request.cookies.get("name")
    pw = request.cookies.get("pw")

    if  username and  pw:
        if hasher(pw) == user_data[username]["pw"]:
            print(type(user_data[username]["chats"]))
            return render_template("chats.html", chats=user_data[username]["chats"], logged=True, username=username, pw=pw, r=random.randint(0, 10000))
        flash("Wrong password", category="error")
    else:
        flash("Please login first", category="error")

    return redirect("/")



@app.route('/add-user-to-chat_user=<targetName>')
def addUserToChat(targetName):
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')

    if hasher(pw) == user_data[username]["pw"]:
        if targetName in user_data[username]["chats"].keys():
            return redirect("/chats#" + targetName)
        user_data[username]["chats"][targetName] = []
        user_data[targetName]["chats"][username] = []
        dumpJson()
        return redirect("/chats#" + targetName)

    else:
        flash("wrong password", category="error")
        return redirect("/")    



@app.route('/send-message_user=<targetName>', methods=['POST'])
def sendMessage(targetName):
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')
    message = request.form.get('message')

    if hasher(pw) == user_data[username]["pw"]:
        user_data[username]["chats"][targetName].append([username, message])
        user_data[targetName]["chats"][username].append([username, message])
        dumpJson()
        return "sent"
    else:
        return "wrong password"


@app.route('/get-my-messages')
def getMyMessages():
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')
    
    if hasher(pw) == user_data[username]['pw']:
        return jsonify(user_data[username]["chats"])
    else:
        return "wrong password"



@app.route('/send-report', methods=['POST'])
def send_report():
    username = request.cookies.get("name")
    pw = request.cookies.get("pw")
    reason = request.form.get("reason")
    moreInfo = request.form.get("moreInfo")
    listingId = request.form.get("listingId")

    if len(moreInfo) == 0 or len(reason) == 0:
        return "cannot be empty"
    if hasher(pw) == user_data[username]["pw"]:
        reports[listingId].append({
            "reason": reason,
            "info": moreInfo,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "from": username
        })
        dumpJson()
        return "success"
    else:
        return "wrong password"





@app.route('/about')
def about():
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if user_data[cookie_name]['pw'] == hasher(cookie_pw):
                return render_template("about.html", logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            else:
                return render_template("about.html",  logged=False, r=random.randint(0, 10000))
        except KeyError:
            return render_template("about.html",   logged=False, r=random.randint(0, 10000))
    else:
        return render_template("about.html",  logged=False, r=random.randint(0, 10000))
    


@app.route('/flash=<flashMessage>_url=<url>')
def customFlash(flashMessage, url):
    print(url)
    flash(flashMessage)
    url = "/" if url == "EMPTY" else "/" + url.replace("SLASH", "/")

    return redirect(url)


    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404





app.run(host='localhost', port=8000, debug=True)
