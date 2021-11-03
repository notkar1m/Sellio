# coding=utf8
import datetime
import sys
from flask import *
import hashlib
import json
import random
import requests
from shortuuid import uuid
import os
import shutil
import time
from countryinfo import CountryInfo
# import pymongo
from flask_pymongo import PyMongo
import base64
app = Flask(__name__)
# client = pymongo.MongoClient(base64.b64decode("bW9uZ29kYitzcnY6Ly9hZG1pbjphZG1pbkBjbHVzdGVyMC56Y3hhOC5tb25nb2RiLm5ldC9kYj9yZXRyeVdyaXRlcz10cnVlJnc9bWFqb3JpdHkmc3NsPXRydWUmc3NsX2NlcnRfcmVxcz1DRVJUX05PTkU=".encode()).decode())
client = PyMongo(app,uri=base64.b64decode("bW9uZ29kYitzcnY6Ly9hZG1pbjphZG1pbkBjbHVzdGVyMC56Y3hhOC5tb25nb2RiLm5ldC9kYj9yZXRyeVdyaXRlcz10cnVlJnc9bWFqb3JpdHkmc3NsPXRydWUmc3NsX2NlcnRfcmVxcz1DRVJUX05PTkU=".encode()).decode())
db = client.db

app.config["SECRET_KEY"] = "SDFL:JSDFLKJSDFlJKSDFlkj"


#region HELPERS
countries = {'Ascension Island': '🇦🇨', 'Andorra': '🇦🇩', 'United Arab Emirates': '🇦🇪', 'Afghanistan': '🇦🇫', 'Antigua & Barbuda': '🇦🇬', 'Anguilla': '🇦🇮', 'Albania': '🇦🇱', 'Armenia': '🇦🇲', 'Angola': '🇦🇴', 'Antarctica': '🇦🇶', 'Argentina': '🇦🇷', 'American Samoa': '🇦🇸', 'Austria': '🇦🇹', 'Australia': '🇦🇺', 'Aruba': '🇦🇼', 'Åland Islands': '🇦🇽', 'Azerbaijan': '🇦🇿', 'Bosnia & Herzegovina': '🇧🇦', 'Barbados': '🇧🇧', 'Bangladesh': '🇧🇩', 'Belgium': '🇧🇪', 'Burkina Faso': '🇧🇫', 'Bulgaria': '🇧🇬', 'Bahrain': '🇧🇭', 'Burundi': '🇧🇮', 'Benin': '🇧🇯', 'St. Barthélemy': '🇧🇱', 'Bermuda': '🇧🇲', 'Brunei': '🇧🇳', 'Bolivia': '🇧🇴', 'Caribbean Netherlands': '🇧🇶', 'Brazil': '🇧🇷', 'Bahamas': '🇧🇸', 'Bhutan': '🇧🇹', 'Bouvet Island': '🇧🇻', 'Botswana': '🇧🇼', 'Belarus': '🇧🇾', 'Belize': '🇧🇿', 'Canada': '🇨🇦', 'Cocos (Keeling) Islands': '🇨🇨', 'Congo - Kinshasa': '🇨🇩', 'Central African Republic': '🇨🇫', 'Congo - Brazzaville': '🇨🇬', 'Switzerland': '🇨🇭', 'Côte d’Ivoire': '🇨🇮', 'Cook Islands': '🇨🇰', 'Chile': '🇨🇱', 'Cameroon': '🇨🇲', 'China': '🇨🇳', 'Colombia': '🇨🇴', 'Clipperton Island': '🇨🇵', 'Costa Rica': '🇨🇷', 'Cuba': '🇨🇺', 'Cape Verde': '🇨🇻', 'Curaçao': '🇨🇼', 'Christmas Island': '🇨🇽', 'Cyprus': '🇨🇾', 'Czechia': '🇨🇿', 'Germany': '🇩🇪', 'Diego Garcia': '🇩🇬', 'Djibouti': '🇩🇯', 'Denmark': '🇩🇰', 'Dominica': '🇩🇲', 'Dominican Republic': '🇩🇴', 'Algeria': '🇩🇿', 'Ceuta & Melilla': '🇪🇦', 'Ecuador': '🇪🇨', 'Estonia': '🇪🇪', 'Egypt': '🇪🇬', 'Western Sahara': '🇪🇭', 'Eritrea': '🇪🇷', 'Spain': '🇪🇸', 'Ethiopia': '🇪🇹', 'European Union': '🇪🇺', 'Finland': '🇫🇮', 'Fiji': '🇫🇯', 'Falkland Islands': '🇫🇰', 'Micronesia': '🇫🇲', 'Faroe Islands': '🇫🇴', 'France': '🇫🇷', 'Gabon': '🇬🇦', 'United Kingdom': '🇬🇧', 'Grenada': '🇬🇩', 'Georgia': '🇬🇪', 'French Guiana': '🇬🇫', 'Guernsey': '🇬🇬', 'Ghana': '🇬🇭', 'Gibraltar': '🇬🇮', 'Greenland': '🇬🇱', 'Gambia': '🇬🇲', 'Guinea': '🇬🇳', 'Guadeloupe': '🇬🇵', 'Equatorial Guinea': '🇬🇶', 'Greece': '🇬🇷', 'South Georgia & South Sandwich Islands': '🇬🇸', 'Guatemala': '🇬🇹', 'Guam': '🇬🇺', 'Guinea-Bissau': '🇬🇼', 'Guyana': '🇬🇾', 'Hong Kong SAR China': '🇭🇰', 'Heard & McDonald Islands': '🇭🇲', 'Honduras': '🇭🇳', 'Croatia': '🇭🇷', 'Haiti': '🇭🇹', 'Hungary': '🇭🇺', 'Canary Islands': '🇮🇨', 'Indonesia': '🇮🇩', 'Ireland': '🇮🇪', 'Israel': '🇮🇱', 'Isle of Man': '🇮🇲', 'India': '🇮🇳', 'British Indian Ocean Territory': '🇮🇴', 'Iraq': '🇮🇶', 'Iran': '🇮🇷', 'Iceland': '🇮🇸', 'Italy': '🇮🇹', 'Jersey': '🇯🇪', 'Jamaica': '🇯🇲', 'Jordan': '🇯🇴', 'Japan': '🇯🇵', 'Kenya': '🇰🇪', 'Kyrgyzstan': '🇰🇬', 'Cambodia': '🇰🇭', 'Kiribati': '🇰🇮', 'Comoros': '🇰🇲', 'St. Kitts & Nevis': '🇰🇳', 'North Korea': '🇰🇵', 'South Korea': '🇰🇷', 'Kuwait': '🇰🇼', 'Cayman Islands': '🇰🇾', 'Kazakhstan': '🇰🇿', 'Laos': '🇱🇦', 'Lebanon': '🇱🇧', 'St. Lucia': '🇱🇨', 'Liechtenstein': '🇱🇮', 'Sri Lanka': '🇱🇰', 'Liberia': '🇱🇷', 'Lesotho': '🇱🇸', 'Lithuania': '🇱🇹', 'Luxembourg': '🇱🇺', 'Latvia': '🇱🇻', 'Libya': '🇱🇾', 'Morocco': '🇲🇦', 'Monaco': '🇲🇨', 'Moldova': '🇲🇩', 'Montenegro': '🇲🇪', 'St. Martin': '🇲🇫', 'Madagascar': '🇲🇬', 'Marshall Islands': '🇲🇭', 'North Macedonia': '🇲🇰', 'Mali': '🇲🇱', 'Myanmar (Burma)': '🇲🇲', 'Mongolia': '🇲🇳', 'Macao Sar China': '🇲🇴', 'Northern Mariana Islands': '🇲🇵', 'Martinique': '🇲🇶', 'Mauritania': '🇲🇷', 'Montserrat': '🇲🇸', 'Malta': '🇲🇹', 'Mauritius': '🇲🇺', 'Maldives': '🇲🇻', 'Malawi': '🇲🇼', 'Mexico': '🇲🇽', 'Malaysia': '🇲🇾', 'Mozambique': '🇲🇿', 'Namibia': '🇳🇦', 'New Caledonia': '🇳🇨', 'Niger': '🇳🇪', 'Norfolk Island': '🇳🇫', 'Nigeria': '🇳🇬', 'Nicaragua': '🇳🇮', 'Netherlands': '🇳🇱', 'Norway': '🇳🇴', 'Nepal': '🇳🇵', 'Nauru': '🇳🇷', 'Niue': '🇳🇺', 'New Zealand': '🇳🇿', 'Oman': '🇴🇲', 'Panama': '🇵🇦', 'Peru': '🇵🇪', 'French Polynesia': '🇵🇫', 'Papua New Guinea': '🇵🇬', 'Philippines': '🇵🇭', 'Pakistan': '🇵🇰', 'Poland': '🇵🇱', 'St. Pierre & Miquelon': '🇵🇲', 'Pitcairn Islands': '🇵🇳', 'Puerto Rico': '🇵🇷', 'Palestinian Territories': '🇵🇸', 'Portugal': '🇵🇹', 'Palau': '🇵🇼', 'Paraguay': '🇵🇾', 'Qatar': '🇶🇦', 'Réunion': '🇷🇪', 'Romania': '🇷🇴', 'Serbia': '🇷🇸', 'Russia': '🇷🇺', 'Rwanda': '🇷🇼', 'Saudi Arabia': '🇸🇦', 'Solomon Islands': '🇸🇧', 'Seychelles': '🇸🇨', 'Sudan': '🇸🇩', 'Sweden': '🇸🇪', 'Singapore': '🇸🇬', 'St. Helena': '🇸🇭', 'Slovenia': '🇸🇮', 'Svalbard & Jan Mayen': '🇸🇯', 'Slovakia': '🇸🇰', 'Sierra Leone': '🇸🇱', 'San Marino': '🇸🇲', 'Senegal': '🇸🇳', 'Somalia': '🇸🇴', 'Suriname': '🇸🇷', 'South Sudan': '🇸🇸', 'São Tomé & Príncipe': '🇸🇹', 'El Salvador': '🇸🇻', 'Sint Maarten': '🇸🇽', 'Syria': '🇸🇾', 'Eswatini': '🇸🇿', 'Tristan Da Cunha': '🇹🇦', 'Turks & Caicos Islands': '🇹🇨', 'Chad': '🇹🇩', 'French Southern Territories': '🇹🇫', 'Togo': '🇹🇬', 'Thailand': '🇹🇭', 'Tajikistan': '🇹🇯', 'Tokelau': '🇹🇰', 'Timor-Leste': '🇹🇱', 'Turkmenistan': '🇹🇲', 'Tunisia': '🇹🇳', 'Tonga': '🇹🇴', 'Turkey': '🇹🇷', 'Trinidad & Tobago': '🇹🇹', 'Tuvalu': '🇹🇻', 'Taiwan': '🇹🇼', 'Tanzania': '🇹🇿', 'Ukraine': '🇺🇦', 'Uganda': '🇺🇬', 'U.S. Outlying Islands': '🇺🇲', 'United Nations': '🇺🇳', 'United States': '🇺🇸', 'Uruguay': '🇺🇾', 'Uzbekistan': '🇺🇿', 'Vatican City': '🇻🇦', 'St. Vincent & Grenadines': '🇻🇨', 'Venezuela': '🇻🇪', 'British Virgin Islands': '🇻🇬', 'U.S. Virgin Islands': '🇻🇮', 'Vietnam': '🇻🇳', 'Vanuatu': '🇻🇺', 'Wallis & Futuna': '🇼🇫', 'Samoa': '🇼🇸', 'Kosovo': '🇽🇰', 'Yemen': '🇾🇪', 'Mayotte': '🇾🇹', 'South Africa': '🇿🇦', 'Zambia': '🇿🇲', 'Zimbabwe': '🇿🇼'}
def hasher(text) -> str: h = hashlib.md5(text.encode()); return h.hexdigest()



def getUserChats(username):
   
    res = list(db.chats.find({"users": username}, {"_id": 0})) 

    if not res: res = []

    return res
     # endregion


# region AUTH
@app.route('/sign-up', methods=['post', 'get'])
def sign_up():
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
    
    if db.users.find_one({"username": name}):
        flash("Username taken", category="error")
        return redirect("/")
    if len(name) > 20:
        flash("Character maximum is 20.", category="error")
        return redirect("/")
    else:

        db.users.insert_one({
            "pw": hasher(pw), 
            "phone": phone,
            "listings": [],
            "favs": [],
            "username": name

        })
        
        cookie = make_response(redirect("/"))
        cookie.set_cookie('name', name)
        cookie.set_cookie('pw', pw)
        cookie.set_cookie('phone', phone)
        flash("Account created, Welcome to Sellio!")
        return cookie


@app.route('/login', methods=['post', 'get'])
def login():
    name = request.form.get('name')
    pw = request.form.get('pw')
    if db.users.find({"username": name}):
        if db.users.find_one({"username": name})["pw"] == hasher(pw):
            cookie = make_response(redirect("/"))
            cookie.set_cookie('name', name)
            cookie.set_cookie('pw', pw)
            flash("Logged in!", category="success")
            return cookie
        else:
            flash("Username or password incorrect." , category="error")
            return redirect("/")
    else:
        flash("Username doesn't exist.", category="error")
        return redirect("/")


@app.route('/logout')
def logout():
    cookie = make_response(redirect("/"))
    cookie.delete_cookie('name')
    cookie.delete_cookie('pw')
    flash("Logged out!", category="success")
    return cookie


# endregion




def getLatestListings():
    
    res = list(db.listings.find().limit(15).sort([('$natural',-1)]))
    return res


@app.route('/')
def index():
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if db.users.find_one({"username":cookie_name})["pw"] == hasher(cookie_pw):
                return render_template("index.html", logged=True,latestListings=getLatestListings(),username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
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
        or db.users.find_one({"username":cookie_name})["pw"] != hasher(cookie_pw)
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
    db.listings.insert_one({
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
    })
    db.users.find_one({"username":request.cookies.get("name")})["listings"].append(listingId)
    db["users"].update_one({"username": request.cookies.get("name")}, {"$push": {"listings": listingId}})
    db.reports.insert_one({"id": listingId, "reports": []})

    return listingId


@app.route('/search', methods=['POST'])
def search():

    text = request.form.get('text')
    tl = text.lower()
    res = []
    for listing in list(db.listings.find({}, {"_id": 0})):
        listingl = listing['title'].lower()
        if listingl in tl or tl.endswith(listingl) or listingl.endswith(tl) or tl.startswith(listingl) or listingl.startswith(tl) or tl == listingl or tl in listingl:
            res.append(listing)
    
    return jsonify({"res":res})


@app.route('/listing/<listingId>')
def lising(listingId):
    if not db.listings.find_one({"id": listingId}):
        flash("Listing not found.", category="error")
        return redirect("/")
    
    cookie_name = request.cookies.get("name")
    cookie_pw = request.cookies.get("pw")
    listing = db.listings.find_one({"id": listingId})
    if (
    not cookie_name
    or not cookie_pw
    or db.users.find_one({"username": cookie_name})["pw"] != hasher(cookie_pw)
    ):

        return render_template('listing.html', listing=listing, r=r.randint(0, 10000))


    return render_template('listing.html', listing=listing, targetPhone=db.users.find_one({"username":listing["owner"]})["phone"] , logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            

@app.route('/user/<targetName>')
def user(targetName):
    targetUser = db.users.find_one({"username":targetName})
    if not targetUser:
        flash("User not found", category="error")
        return redirect('/')
    phone = targetUser["phone"]
    targetListings = targetUser["listings"]
    listingsRes = [db.listings.find_one({"id":l}) for l in targetListings]
    if not request.cookies.get("name") or not request.cookies.get("pw"):
        return render_template("profile.html", phone=phone, listings=listingsRes,targetName=targetName,logged=False, r=random.randint(0, 10000))

    return render_template("profile.html", phone=phone, listings=listingsRes,targetName=targetName,logged=True, username=request.cookies.get("name"), pw=request.cookies.get("pw"), r=random.randint(0, 10000))



@app.route('/add-to-fav_listingId=<listingId>')
def addToFav(listingId):
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')

    if hasher(pw) != db.users.find_one({"username": username})["pw"]:
        return jsonify({"res": "Wrong password"})

    if db.listings.find_one({"id": listingId}) and listingId not in db.users.find_one({"username": username})["favs"]: 
        db["users"].update_one({"username": username}, {"$push": {"favs": listingId}})
        return jsonify({"res": "success"})
    else:
        return jsonify({"res":"listing not found"})

@app.route('/remove-from-fav_listingId=<listingId>')
def removeFromFav(listingId):
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')

    if hasher(pw) != db.users.find_one({"username": username})["pw"]:
        return jsonify({"res": "Wrong password"})

    if db.listings.find_one({"id": listingId}) and listingId in db.users.find_one({"username": username})["favs"]: 
        db.users.update_one({"username": username}, {"$pull": {"favs": listingId}})
        return jsonify({"res": "success"})
    else:
        return jsonify({"res":"listing not found"})


@app.route('/get-my-favs')
def getMyFavs():
    pw = request.cookies.get('pw')
    username = request.cookies.get('name')
    if hasher(pw) == db.users.find_one({"username": username})["pw"]:
        return jsonify({"res": db.users.find_one({"username": username})["favs"]})
    else:
        return jsonify({"res": "wrong password"}) 


@app.route('/favorites')
def favorites():
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if db.users.find_one({"username": cookie_name})["pw"] == hasher(cookie_pw):
                favListings = []
                for listing in db.users.find_one({"username": cookie_name})["favs"]:
                    favListings.append(db.listings.find_one({"id": listing}))
                

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
    return jsonify({"res":list(db.listings.find({"category": category}, {"_id":0}))})



@app.route('/remove-listing_id=<id>')
def removeListing(id):
    pw = request.cookies.get('pw')
    username = request.cookies.get('name')
    if hasher(pw) != db.users.find_one({"username": username})["pw"]:
        return jsonify({"res":"wrong password"})
    if not db.listings.find_one({"id": id}):
        return jsonify({"res":"listing not found"})

    for _ in range(len(db.listings.find_one({"id": id})["imageType"])):
        try:
            shutil.rmtree("./static/listing_images/" + id )
        except:
            pass
    db.users.update_one({"username": username}, {"$pull": {"listings": id}})
    db.listings.delete_one({"id":id})
    db.users.update_one({"username": username}, {"$pull": {"favs": id}})
    return jsonify({"res":"success"})



@app.route('/change-pfp', methods=['POST'])
def changePfp():
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')
    if hasher(pw) == db.users.find_one({"username": username})["pw"]:
        newPfp = request.files["image"]
        newPfp.save("static/pfps/" +username + os.path.splitext(newPfp.filename)[1])
        # user_data[username]["pfp"] = "/static/pfp/" + username + os.path.splitext(newPfp.filename)[1]
        return "success"
    else:
        return "wrong password"



@app.route('/chats')
def chatsPage():
    username = request.cookies.get("name")
    pw = request.cookies.get("pw")

    if  username and  pw:
        if hasher(pw) == db.users.find_one({"username": username})["pw"]:
            userChats = getUserChats(username)

            return render_template("chats.html", logged=True, username=username ,pw=pw, chats=userChats,r=random.randint(0, 10000))
        flash("Wrong password", category="error")
    else:
        flash("Please login first", category="error")

    return redirect("/")



@app.route('/add-user-to-chat_user=<targetName>')
def addUserToChat(targetName):
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')

    if hasher(pw) == db.users.find_one({"username": username})["pw"]:
        userChats = getUserChats(username)
        if targetName in [item for sublist in [x["users"] for x in userChats] for item in sublist]:
            return redirect("/chats#" + targetName)
        db.chats.insert_one({"users":[username, targetName], "chat": []})
        return redirect("/chats#" + targetName)

    else:
        flash("wrong password", category="error")
        return redirect("/")    



@app.route('/send-message_user=<targetName>', methods=['POST'])
def sendMessage(targetName):
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')
    message = request.form.get('message')
    if(len(message) > 2000):
        return "message too long"

    if hasher(pw) == db.users.find_one({"username": username})["pw"]:
        db.chats.update_one({"users": {"$all": [username, targetName]}}, {"$push": {"chat":[username, message]}})
        return "sent"
    else:
        return "wrong password"


@app.route('/get-my-messages')
def getMyMessages():
    username = request.cookies.get('name')
    pw = request.cookies.get('pw')
    
    if hasher(pw) == db.users.find_one({"username": username})["pw"]:
        return jsonify(getUserChats(username))
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
    if hasher(pw) == db.users.find_one({"username": username})["pw"]:
        db.reports.update_one({"id":listingId},{"$push": {"reports":{
            "reason": reason,
            "info": moreInfo,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "from": username
        }}})
        return "success"
    else:
        return "wrong password"





@app.route('/about')
def about():
    cookie_name = request.cookies.get('name')
    cookie_pw = request.cookies.get('pw')
    if cookie_name and cookie_pw:
        try:
            if db.users.find_one({"username": cookie_name})["pw"] == hasher(cookie_pw):
                return render_template("about.html", logged=True, username=cookie_name, pw=cookie_pw, r=random.randint(0, 10000))
            else:
                return render_template("about.html",  logged=False, r=random.randint(0, 10000))
        except KeyError:
            return render_template("about.html",   logged=False, r=random.randint(0, 10000))
    else:
        return render_template("about.html",  logged=False, r=random.randint(0, 10000))
    

@app.route('/get-chat-length')
def get_chat_length():
        username = request.cookies.get("name")
        pw = request.cookies.get("pw")
     
        if hasher(pw) == db.users.find_one({"username": username})["pw"]:
            res = len([item for sublist in [x["chat"] for x in list(db.chats.find({"users": username}))] for item in sublist] )
            return jsonify({"res":res})
        else:
            return "wrong password"
    
@app.route('/search-users_q=<q>')
def search_users(q):
    tl = q.lower()
    res = []
    for user in db.users.distinct("username"):
        userl = user.lower()
        if userl in tl or tl.endswith(userl) or userl.endswith(tl) or tl.startswith(userl) or userl.startswith(tl) or tl == userl or tl in userl:
            res.append(user)

    return jsonify({"res":res})

    



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
