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
countries = {'Ascension Island': '๐ฆ๐จ', 'Andorra': '๐ฆ๐ฉ', 'United Arab Emirates': '๐ฆ๐ช', 'Afghanistan': '๐ฆ๐ซ', 'Antigua & Barbuda': '๐ฆ๐ฌ', 'Anguilla': '๐ฆ๐ฎ', 'Albania': '๐ฆ๐ฑ', 'Armenia': '๐ฆ๐ฒ', 'Angola': '๐ฆ๐ด', 'Antarctica': '๐ฆ๐ถ', 'Argentina': '๐ฆ๐ท', 'American Samoa': '๐ฆ๐ธ', 'Austria': '๐ฆ๐น', 'Australia': '๐ฆ๐บ', 'Aruba': '๐ฆ๐ผ', 'รland Islands': '๐ฆ๐ฝ', 'Azerbaijan': '๐ฆ๐ฟ', 'Bosnia & Herzegovina': '๐ง๐ฆ', 'Barbados': '๐ง๐ง', 'Bangladesh': '๐ง๐ฉ', 'Belgium': '๐ง๐ช', 'Burkina Faso': '๐ง๐ซ', 'Bulgaria': '๐ง๐ฌ', 'Bahrain': '๐ง๐ญ', 'Burundi': '๐ง๐ฎ', 'Benin': '๐ง๐ฏ', 'St. Barthรฉlemy': '๐ง๐ฑ', 'Bermuda': '๐ง๐ฒ', 'Brunei': '๐ง๐ณ', 'Bolivia': '๐ง๐ด', 'Caribbean Netherlands': '๐ง๐ถ', 'Brazil': '๐ง๐ท', 'Bahamas': '๐ง๐ธ', 'Bhutan': '๐ง๐น', 'Bouvet Island': '๐ง๐ป', 'Botswana': '๐ง๐ผ', 'Belarus': '๐ง๐พ', 'Belize': '๐ง๐ฟ', 'Canada': '๐จ๐ฆ', 'Cocos (Keeling) Islands': '๐จ๐จ', 'Congo - Kinshasa': '๐จ๐ฉ', 'Central African Republic': '๐จ๐ซ', 'Congo - Brazzaville': '๐จ๐ฌ', 'Switzerland': '๐จ๐ญ', 'Cรดte dโIvoire': '๐จ๐ฎ', 'Cook Islands': '๐จ๐ฐ', 'Chile': '๐จ๐ฑ', 'Cameroon': '๐จ๐ฒ', 'China': '๐จ๐ณ', 'Colombia': '๐จ๐ด', 'Clipperton Island': '๐จ๐ต', 'Costa Rica': '๐จ๐ท', 'Cuba': '๐จ๐บ', 'Cape Verde': '๐จ๐ป', 'Curaรงao': '๐จ๐ผ', 'Christmas Island': '๐จ๐ฝ', 'Cyprus': '๐จ๐พ', 'Czechia': '๐จ๐ฟ', 'Germany': '๐ฉ๐ช', 'Diego Garcia': '๐ฉ๐ฌ', 'Djibouti': '๐ฉ๐ฏ', 'Denmark': '๐ฉ๐ฐ', 'Dominica': '๐ฉ๐ฒ', 'Dominican Republic': '๐ฉ๐ด', 'Algeria': '๐ฉ๐ฟ', 'Ceuta & Melilla': '๐ช๐ฆ', 'Ecuador': '๐ช๐จ', 'Estonia': '๐ช๐ช', 'Egypt': '๐ช๐ฌ', 'Western Sahara': '๐ช๐ญ', 'Eritrea': '๐ช๐ท', 'Spain': '๐ช๐ธ', 'Ethiopia': '๐ช๐น', 'European Union': '๐ช๐บ', 'Finland': '๐ซ๐ฎ', 'Fiji': '๐ซ๐ฏ', 'Falkland Islands': '๐ซ๐ฐ', 'Micronesia': '๐ซ๐ฒ', 'Faroe Islands': '๐ซ๐ด', 'France': '๐ซ๐ท', 'Gabon': '๐ฌ๐ฆ', 'United Kingdom': '๐ฌ๐ง', 'Grenada': '๐ฌ๐ฉ', 'Georgia': '๐ฌ๐ช', 'French Guiana': '๐ฌ๐ซ', 'Guernsey': '๐ฌ๐ฌ', 'Ghana': '๐ฌ๐ญ', 'Gibraltar': '๐ฌ๐ฎ', 'Greenland': '๐ฌ๐ฑ', 'Gambia': '๐ฌ๐ฒ', 'Guinea': '๐ฌ๐ณ', 'Guadeloupe': '๐ฌ๐ต', 'Equatorial Guinea': '๐ฌ๐ถ', 'Greece': '๐ฌ๐ท', 'South Georgia & South Sandwich Islands': '๐ฌ๐ธ', 'Guatemala': '๐ฌ๐น', 'Guam': '๐ฌ๐บ', 'Guinea-Bissau': '๐ฌ๐ผ', 'Guyana': '๐ฌ๐พ', 'Hong Kong SAR China': '๐ญ๐ฐ', 'Heard & McDonald Islands': '๐ญ๐ฒ', 'Honduras': '๐ญ๐ณ', 'Croatia': '๐ญ๐ท', 'Haiti': '๐ญ๐น', 'Hungary': '๐ญ๐บ', 'Canary Islands': '๐ฎ๐จ', 'Indonesia': '๐ฎ๐ฉ', 'Ireland': '๐ฎ๐ช', 'Israel': '๐ฎ๐ฑ', 'Isle of Man': '๐ฎ๐ฒ', 'India': '๐ฎ๐ณ', 'British Indian Ocean Territory': '๐ฎ๐ด', 'Iraq': '๐ฎ๐ถ', 'Iran': '๐ฎ๐ท', 'Iceland': '๐ฎ๐ธ', 'Italy': '๐ฎ๐น', 'Jersey': '๐ฏ๐ช', 'Jamaica': '๐ฏ๐ฒ', 'Jordan': '๐ฏ๐ด', 'Japan': '๐ฏ๐ต', 'Kenya': '๐ฐ๐ช', 'Kyrgyzstan': '๐ฐ๐ฌ', 'Cambodia': '๐ฐ๐ญ', 'Kiribati': '๐ฐ๐ฎ', 'Comoros': '๐ฐ๐ฒ', 'St. Kitts & Nevis': '๐ฐ๐ณ', 'North Korea': '๐ฐ๐ต', 'South Korea': '๐ฐ๐ท', 'Kuwait': '๐ฐ๐ผ', 'Cayman Islands': '๐ฐ๐พ', 'Kazakhstan': '๐ฐ๐ฟ', 'Laos': '๐ฑ๐ฆ', 'Lebanon': '๐ฑ๐ง', 'St. Lucia': '๐ฑ๐จ', 'Liechtenstein': '๐ฑ๐ฎ', 'Sri Lanka': '๐ฑ๐ฐ', 'Liberia': '๐ฑ๐ท', 'Lesotho': '๐ฑ๐ธ', 'Lithuania': '๐ฑ๐น', 'Luxembourg': '๐ฑ๐บ', 'Latvia': '๐ฑ๐ป', 'Libya': '๐ฑ๐พ', 'Morocco': '๐ฒ๐ฆ', 'Monaco': '๐ฒ๐จ', 'Moldova': '๐ฒ๐ฉ', 'Montenegro': '๐ฒ๐ช', 'St. Martin': '๐ฒ๐ซ', 'Madagascar': '๐ฒ๐ฌ', 'Marshall Islands': '๐ฒ๐ญ', 'North Macedonia': '๐ฒ๐ฐ', 'Mali': '๐ฒ๐ฑ', 'Myanmar (Burma)': '๐ฒ๐ฒ', 'Mongolia': '๐ฒ๐ณ', 'Macao Sar China': '๐ฒ๐ด', 'Northern Mariana Islands': '๐ฒ๐ต', 'Martinique': '๐ฒ๐ถ', 'Mauritania': '๐ฒ๐ท', 'Montserrat': '๐ฒ๐ธ', 'Malta': '๐ฒ๐น', 'Mauritius': '๐ฒ๐บ', 'Maldives': '๐ฒ๐ป', 'Malawi': '๐ฒ๐ผ', 'Mexico': '๐ฒ๐ฝ', 'Malaysia': '๐ฒ๐พ', 'Mozambique': '๐ฒ๐ฟ', 'Namibia': '๐ณ๐ฆ', 'New Caledonia': '๐ณ๐จ', 'Niger': '๐ณ๐ช', 'Norfolk Island': '๐ณ๐ซ', 'Nigeria': '๐ณ๐ฌ', 'Nicaragua': '๐ณ๐ฎ', 'Netherlands': '๐ณ๐ฑ', 'Norway': '๐ณ๐ด', 'Nepal': '๐ณ๐ต', 'Nauru': '๐ณ๐ท', 'Niue': '๐ณ๐บ', 'New Zealand': '๐ณ๐ฟ', 'Oman': '๐ด๐ฒ', 'Panama': '๐ต๐ฆ', 'Peru': '๐ต๐ช', 'French Polynesia': '๐ต๐ซ', 'Papua New Guinea': '๐ต๐ฌ', 'Philippines': '๐ต๐ญ', 'Pakistan': '๐ต๐ฐ', 'Poland': '๐ต๐ฑ', 'St. Pierre & Miquelon': '๐ต๐ฒ', 'Pitcairn Islands': '๐ต๐ณ', 'Puerto Rico': '๐ต๐ท', 'Palestinian Territories': '๐ต๐ธ', 'Portugal': '๐ต๐น', 'Palau': '๐ต๐ผ', 'Paraguay': '๐ต๐พ', 'Qatar': '๐ถ๐ฆ', 'Rรฉunion': '๐ท๐ช', 'Romania': '๐ท๐ด', 'Serbia': '๐ท๐ธ', 'Russia': '๐ท๐บ', 'Rwanda': '๐ท๐ผ', 'Saudi Arabia': '๐ธ๐ฆ', 'Solomon Islands': '๐ธ๐ง', 'Seychelles': '๐ธ๐จ', 'Sudan': '๐ธ๐ฉ', 'Sweden': '๐ธ๐ช', 'Singapore': '๐ธ๐ฌ', 'St. Helena': '๐ธ๐ญ', 'Slovenia': '๐ธ๐ฎ', 'Svalbard & Jan Mayen': '๐ธ๐ฏ', 'Slovakia': '๐ธ๐ฐ', 'Sierra Leone': '๐ธ๐ฑ', 'San Marino': '๐ธ๐ฒ', 'Senegal': '๐ธ๐ณ', 'Somalia': '๐ธ๐ด', 'Suriname': '๐ธ๐ท', 'South Sudan': '๐ธ๐ธ', 'Sรฃo Tomรฉ & Prรญncipe': '๐ธ๐น', 'El Salvador': '๐ธ๐ป', 'Sint Maarten': '๐ธ๐ฝ', 'Syria': '๐ธ๐พ', 'Eswatini': '๐ธ๐ฟ', 'Tristan Da Cunha': '๐น๐ฆ', 'Turks & Caicos Islands': '๐น๐จ', 'Chad': '๐น๐ฉ', 'French Southern Territories': '๐น๐ซ', 'Togo': '๐น๐ฌ', 'Thailand': '๐น๐ญ', 'Tajikistan': '๐น๐ฏ', 'Tokelau': '๐น๐ฐ', 'Timor-Leste': '๐น๐ฑ', 'Turkmenistan': '๐น๐ฒ', 'Tunisia': '๐น๐ณ', 'Tonga': '๐น๐ด', 'Turkey': '๐น๐ท', 'Trinidad & Tobago': '๐น๐น', 'Tuvalu': '๐น๐ป', 'Taiwan': '๐น๐ผ', 'Tanzania': '๐น๐ฟ', 'Ukraine': '๐บ๐ฆ', 'Uganda': '๐บ๐ฌ', 'U.S. Outlying Islands': '๐บ๐ฒ', 'United Nations': '๐บ๐ณ', 'United States': '๐บ๐ธ', 'Uruguay': '๐บ๐พ', 'Uzbekistan': '๐บ๐ฟ', 'Vatican City': '๐ป๐ฆ', 'St. Vincent & Grenadines': '๐ป๐จ', 'Venezuela': '๐ป๐ช', 'British Virgin Islands': '๐ป๐ฌ', 'U.S. Virgin Islands': '๐ป๐ฎ', 'Vietnam': '๐ป๐ณ', 'Vanuatu': '๐ป๐บ', 'Wallis & Futuna': '๐ผ๐ซ', 'Samoa': '๐ผ๐ธ', 'Kosovo': '๐ฝ๐ฐ', 'Yemen': '๐พ๐ช', 'Mayotte': '๐พ๐น', 'South Africa': '๐ฟ๐ฆ', 'Zambia': '๐ฟ๐ฒ', 'Zimbabwe': '๐ฟ๐ผ'}
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
    if db.users.find_one({"username": name}):
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

        return render_template('listing.html', listing=listing, r=random.randint(0, 10000))


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
