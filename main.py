from flask import Flask, render_template, url_for, request, session, redirect, flash, session
import jsonify
import math
import requests, json
from replit import db
import random
import zipcodes
app = Flask(__name__)
app.secret_key = 'ifjeriogjeriogjrtoig'

api_key = "Your_API_Key"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def getTemp(zip):
  city = zipcodes.matching(str(zip))['city']

  complete_url = base_url + "appid=" + api_key + "&q=" + city
  response = requests.get(complete_url)
  x = response.json()
  if x["cod"] != "404":
    temp = int(x["main"]["temp"])
    ftemp = 1.8*(temp-273) + 32

    return ftemp
    

@app.route('/', methods=["GET"])
def index():
    return redirect('/dashboard')

poss = ["Light Blue","Dark Blue", "Black", "Red", "Green", "White", "Gray", "Purple", "Pink", "Yellow", "Orange", "Brown","Magenta", "Tan"]
res = "9990099090090900900990009909999999999999090090099090090900900999000909999990999089999998980890090990909990000909909809900009099090009800090000908998000900999099909900990090099000090899909099900980"

dct = [{"Light Blue":"img2/lightblueshirt.png", "Dark Blue":"img2/darkblueshirt.png","Black":"img2/blackshirt.png","Red":"img2/redshirt.png","Green":"img2/greenshirt.png","White":"img2/whiteshirt.png","Gray":"img2/grayshirt.png","Purple":"img2/purpleshirt.png","Pink":"img2/pinkshirt.png","Yellow":"img2/yellowshirt.png","Orange":"img2/orangeshirt.png","Brown":"img2/brownshirt.png","Magenta":"img2/magentashirt.png","Tan":"img2/tanshirt.png"}, {"Light Blue":"img3/lightbluepants.png", "Dark Blue":"img3/darkbluepants.png","Black":"img3/blackpants.png","Red":"img3/redpants.png","Green":"img3/greenpants.png","White":"img3/whitepants.png","Gray":"img3/graypants.png","Purple":"img3/purplepants.png","Pink":"img3/pinkpants.png","Yellow":"img3/yellowpants.png","Orange":"img3/orangepants.png","Brown":"img3/brownpants.png","Magenta":"img3/magentapants.png","Tan":"img3/tanpants.png"}]
def num(clr):
    for i in range(14):
        if poss[i] == clr:
            return i
def check(x,y):
    return res[14*x + y]=="9"

def conv(x):
  if str(x)== str("Shirt"):
    return 0
  else:
    return 1
@app.route('/upload', methods = ["GET", "POST"])
def add():
    if request.method =="GET":
        return render_template("upload.html")
    else:
        color =str(request.form["color"])
        typ = str(request.form["type"])
        quan = int(request.form["used"])
        quan2 = int(request.form["left"])
        id = str(random.randint(10000, 100000))
        session["all"].append(str(id))
        session[str(id)]=[typ, color, quan, quan2, id, dct[conv(typ)][color]]
        return redirect("/dashboard")
  
@app.route("/dashboard", methods = ["GET"])
def dash():
    lst = []
    count = 0
    stuff = []
    if "all" not in session.keys():
        session["all"] = []
    for d in session["all"]:
        if count%4==0:
            stuff.append([])
        count+=1
        stuff[-1].append(session[d])
    return render_template("dashboard.html", lst = stuff, dct=dct)

@app.route('/get_ip')
def getip():
  return f"{request.environ['REMOTE_ADDR']}"

@app.route("/edit/<id>", methods = ["GET", "POST"])
def edit(id):
    id = str(id)
    if request.method == "GET":
	    return render_template("details.html", inf = session[str(id)], dct=dct, img = dct[conv(session[str(id)][1])][session[str(id)][1]])
    else:
        used = request.form["used"]
        left = request.form["left"]
        session[str(id)][2] = int(used)
        session[str(id)][3] = int(left)
        return render_template("details.html", inf = session[str(id)], dct=dct, img = dct[conv(session[str(id)][0])][session[str(id)][1]])
    
@app.route("/settings", methods = ["GET", "POST"])
def settings():
    if request.method == "POST":
        nm = request.form["name"]
        lc = request.form["location"]
        if nm != "":
            session["name"] = nm
        if lc != "":
            session["loc"] = lc
    return render_template("settings.html", location = session["loc"], name = session["name"])

@app.route("/outfits", methods=["GET"])
def outfits():
  pairs = []
  for id in session["all"]:
    for id2 in session["all"]:
      if session[id][3] == 0 or session[id2][3] ==0 or session[id][0]!= "Shirt" or session[id2][0] != "Pant":
        continue
      num1 = num(session[id][1])
      num2 = num(session[id2][1])
      if check(num1, num2):
        print(session[id])
        print(session[id2])
        pairs.append([session[id], session[id2], dct[conv(session[id][0])][session[id][1]], dct[conv(session[id2][0])][session[id2][1]]])
  prs= []
  cnt = 0
  for x in pairs:
    if cnt%2==0:
      prs.append([])
    prs[-1].append(x)
    cnt+=1
  return render_template("outfits.html", lst = prs)
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
