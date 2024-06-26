import base64
from email import message
from turtle import st
from dns.message import Message
from flask import Flask, render_template, url_for, request, redirect,flash,session,jsonify
from flask.scaffold import F
from flask_pymongo import PyMongo
from flask_wtf.form import FlaskForm
from pymongo import MongoClient
import passlib
from passlib.context import CryptContext
from passlib.hash import bcrypt_sha256,argon2,ldap_salted_md5,md5_crypt
import time
from datetime import timedelta , datetime
import smtplib
from email.message import EmailMessage
import socket,os
from functools import wraps
from gridfs import*
from bson import ObjectId
from flask_hcaptcha import hCaptcha
from flask_wtf import RecaptchaField,FlaskForm
from wtforms import *
from wtforms.validators import EqualTo, InputRequired
from flask_wtf.csrf import CSRFProtect
from wtforms.csrf.session import SessionCSRF 
from datetime import timedelta
import email_validator 
import random
from flask_mail import Mail,Message

import base64
from bson.binary import Binary
from werkzeug.utils import secure_filename

import PIL
from PIL import Image

import markupsafe
from markupsafe import escape , Markup

#paypal 
import paypalrestsdk

#personal modules imports
from mods.settings import csrf,upload_folder,mongo#hcaptcha

from mods.datas import tech,enta,sports,rel,buss_invest,tags1

from mods.methods import login_required,reset_session_required,get_the_token,capture_pyp,create_order

ip = socket. gethostbyname(socket. gethostname())
ipst = str(ip)
application = Flask(__name__)

#images
upload_folder = 'static/images'
application.config['UPLOAD_FOLDER'] = upload_folder
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg' , 'gif' , 'tiff' ,'heif' ,'raw' , 'psd'])


application.permanent_session_lifetime = timedelta(days=30)

Hash_passcode = CryptContext(schemes=["sha256_crypt", "ldap_salted_md5" ,"des_crypt" ],sha256_crypt__min_rounds=131072)

users = mongo.db.users
verif = mongo.db.verify_email
cleos = mongo.db.cleos
post_db = mongo.db.cleos

 
 #routes import
 
from mods  import routes  
@application.route('/',methods = ["POST","GET"])
def home():
    if request.method == "POST" and hcaptcha.verify():
        email = request.form['email']
        existing_user  = users.find_one({'email':email} )
        if existing_user:
                passcode = request.form['passcode']
                v = str(existing_user['verified'])

                existing_pass = existing_user['password']
                if Hash_passcode.verify(passcode,existing_pass):
                    username = existing_user['username']
                    if username in session:
                        fa = existing_user['tags']
                        if len(fa) < 5:
                             return redirect(url_for('choose_tags'))
                        if v == 0:
                            return redirect(url_for('complete_regist'))
                        else:
                            return redirect(url_for('feed'))
                    else:    
                        session_time = request.form.get("session_time") 
                        if  session_time == 2:
                            session.parmanent = True
                        session['login_user'] = email
                        fa = existing_user['tags']
                        if len(fa) < 5:
                            return redirect(url_for('choose_tags'))
                        else:    
                            return redirect(url_for('feed'))   
    return render_template("index.html")


@application.route('/reset_pass/', methods = ['POST','GET'])
def  reset_pass():
    reset_db = mongo.db.pass_reset
    code = random.randint(145346 , 976578)
    code = str(code)
    if request.method == "POST":
        email = request.form['email']
        existing = users.find_one({'email':email} )
        if existing:
            '''
            Send message here with the code
            '''
            now = datetime.now()
            r_now =  now.strftime("Date  %Y:%m:%d: Time %H:%M:%S")
            session['rset'] = email
            reset_db.insert_one({"email" : email , "code" : code , "time_in" : r_now})
            return redirect(url_for("enter_code"))      
        else:
            return redirect(url_for('register'))
    return render_template('reset_pass.html')
@application.route('/enter_code/' , methods = ['POST','GET'])
def enter_code():
    email = session['rset']
    if email in session:
        if request.method == "POST":
            reset_db = mongo.db.pass_reset
            code = request.form['code']
            mailed = email
            legit = reset_db.find_one({"email" : email})
            if legit:
                legit_code = legit["code"]
                now = datetime.now()
                now = now.strftime("Date  %Y:%m:%d: Time %H:%M:%S")
                req_time = legit['time_in']
                diff = now - req_time
                if code == legit_code and diff < 7:
                    return redirect(url_for('peopleass'))  
                if diff > 7:
                    return redirect(url_for('reset_pass' ))
            else:
                return redirect(url_for('reset_pass'))
    else:
        return redirect(url_for('reset_pass'))
            
    return render_template('enter_code.html')

                
@application.route('/login/' , methods = ['POST','GET'])
def login():
    if request.method == "POST"  hcaptcha.verify():
        email = request.form['email']
        existing_user  = users.find_one({'email':email} )
        if existing_user:
                passcode = request.form['passcode']

                existing_pass = existing_user['password']
                v = str(existing_user['verified'])
                if Hash_passcode.verify(passcode,existing_pass)  :
                    username = existing_user['username']
                    if username in session:
                        fa = existing_user['tags']
                        if len(fa) < 5:
                             return redirect(url_for('choose_tags'))
                        if v == 0:
                            return redirect(url_for('complete_regist'))
                        else:
                            return redirect(url_for('feed'))
                    else:    
                        session_time = request.form.get("session_time") 
                        if  session_time == 2:
                            session.parmanent = True
                        session['login_user'] = email
                        fa = existing_user['tags']
                        if len(fa) < 5:
                            return redirect(url_for('choose_tags'))
                        else:    
                            return redirect(url_for('feed'))
    return render_template('login.html')

@application.route('/logout/' , methods = ['POST','GET'])
@login_required
def logout():
    if request.method == "POST":
        if request.form['sub'] == "Yes":
            session.pop('login_user', None)
            return redirect(url_for('login'))
        else:
            return redirect(url_for('feed')) 
    return render_template('logout.html')

@application.route('/register/',methods = ['POST','GET'])
def register():
    
    if request.method == "POST" and "img" in request.files:
        
        pic = request.files['img']
        
        email = request.form['email']
        
        username =  request.form['username']
        
        passc = request.form['passc']
        
        passc2 = request.form['passc2']
        
        hashed = Hash_passcode.hash(passc2)
        
        filename = pic.filename
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
        registered = users.find_one({"email":email})
        if registered:
            mess = "You are already registered,please Log in"
            return redirect(url_for('home'))
        if passc == passc2  and not registered:
            if allowed_file(filename):
                fl = email.replace("." , "")
                os.mkdir("static/images/" + fl)
                pt = "static/images/" + fl + "/"
                des = fl + "/" + filename
                dess = "static/images/" + des
                
                pic.save("static/images/" + des)
                image1 = "static/images/" + des
                image = Image.open(image1)
                new = image.convert("RGB")
                new.save(pt + fl + '.jpg')
                image = pt +fl + ".jpg"
                os.remove(dess)
            
            mess = "Registerd Successfully" 
            favs = []
            tags = []
            users.insert_one({"email":email ,'username':username , "password":hashed , 
                             "favs" : favs , "tags" : tags , "verified" :0 , 'saved' : [] })
            
            if users.find_one({"email":email}):
                code = random.randint(145346 , 976578)
                code = str(code)
                session['login_user'] = email
                verif.insert_one({"email" : email , "code" : code })
                #send the code Here
                
                return redirect(url_for('complete_regist'))
    return render_template('register.html')
    
@application.route('/choose_tags/' , methods = ['POST','GET'])
@login_required
def choose_tags():
    the_tags = tags1
    user_email = session['login_user']
    if request.method == "POST":
        aaction = request.form.getlist('tags')
        user_db = mongo.db.users
        
        list2 = random.sample(the_tags , 6)
        user = user_db.find_one({"email" : user_email})
        if len(aaction) < 5:
            em_tags = user['tags']
            for x in list2:
                em_tags.append(x)
            user_db.find_one_and_update({"email" : user_email} ,{ '$set' :  {"tags": em_tags}} )
            return redirect(url_for('choose_favs'))
        else:
            em_tags = user['tags']
            for y in aaction:
                em_tags.append(y)
            user_db.find_one_and_update({"email" : user_email} ,{ '$set' :  {"tags": em_tags}} )
            return redirect(url_for('feed' ))      
    return render_template('choose_tags.html' , tags = the_tags)


@application.route('/choose_favs/' , methods = ['POST','GET'])
@login_required
def choose_favs():
    user_email = session['login_user']
    user_db = mongo.db.users
    user = user_db.find_one({"email" : user_email})
    em_favs = user['favs']
    favs_tags = user['tags']
    all_posts= post_db.find()
    f = []
    for k in all_posts:
            ok = k['tags']
            for x in favs_tags:
                one = x
                if one in ok:
                    f.append(k)
    for ps in f:
        owner = ps['owner']
        em_favs.append(owner)
        user_db.find_one_and_update({"email" : user_email} ,{ '$set' :  {"favs": em_favs}} )
        
    
    favs_tags =   ['music' , 'sports' , 'crypto' ,'technology' , 'real estate' , 'nature' , 'art' , 'gaming' , 'nft' ,'politics' ,'elon' , 'watch' ,
                    'memes' , 'russia'
                    ]
    f = []
    for k in all_posts:
            ok = k['tags']
            for x in favs_tags:
                one = x
                if one in ok:
                    f.append(k)
    for ps in f:
        owner = ps['owner']
        e_favs = []
        e_favs.append(owner)
    new_favs = user['favs']
    
    for t in new_favs:
        if t in e_favs:
            e_favs.remove(t)
            user_db.find_one_and_update({"email" : user_email} ,{ '$set' :  {"favs": e_favs}} )
    return render_template('choose_favs.html')

@application.route('/feed/' , methods = ['POST','GET'])
@login_required
def feed():
    post_db = mongo.db.cleos
    em = post_db.find()
    user = mongo.db.users
    trending_db = mongo.db.trending
    randomly = post_db.find().limit(100)
    render_array = []
    render_array.extend(randomly)
    #based on following people
    user_email = session['login_user']
    the_user = users.find_one({"email" : user_email})
    favs = the_user["favs"]
    fav_arr = []
    if len(favs) <10:
        count = 3
    else:
        count = 2
    for x in favs:         
        user = x
        documentz = post_db.find({"owner" : user }).limit(count)
        for kk in documentz:
            if not kk in render_array:
                fav_arr.extend(documentz)      
    render_array.extend(fav_arr)

    #based on tags
    my_tags = the_user["tags"]
    for y in my_tags:
        indiv_tags  = y
        #relevant = trending_db.find({"tags" : tags})
        arr1 = []
        all_posts= post_db.find().limit(300)
        for x in all_posts:
            tags = x['tags']
            if indiv_tags in tags:
                if not  x in render_array: 
                    arr1.append(x)        
    render_array.extend(arr1)
    random.shuffle(render_array)
    
        
    #view link functionality
    if request.method == "POST":
        dt = request.get_json()
        name = data["name"]
        age = data["age"]
        #view the link here
        the_id = request.form['id']
        if request.form['sub'] == "View Link": 
            session["linky"] = the_id
            return redirect(url_for('view_link' ))
            
        
        #like the post
        if request.form['sub'] == "Like":
            the_post = post_db.find_one({"post_id" : the_id})
            likes= the_post['likes']
            total_likes = len(likes)
            clicker = session['login_user']
            
            
            if clicker in likes:
                likes.remove(clicker)
                total_likes = len(likes)
                post_db.find_one_and_update({"post_id" : the_id} ,{ '$set' :  {"likes": likes  , 'total_likes' : total_likes }} )
                b_color = "red"
            else:
                likes.append(clicker) 
                total_likes = len(likes)
                post_db.find_one_and_update({"post_id" : the_id} ,{ '$set' :  {"likes": likes  , 'total_likes' : total_likes}} )
                b_color = "less"                   
    return render_template('main.html' , arr = render_array , fav = fav_arr , email = user_email )


@application.route('/profile/' , methods = ['POST','GET'])  
@login_required
def profile():
    trend = mongo.db.trending
    me = session['login_user']
    me2 = me.replace("." , "")
    the_arr = ["electric car" , "rap" , "football"]
    acc = users.find_one({"email" : me})
    favs = acc['favs']
    tags = acc['tags']
    user = acc['username']
    minez = []
    my_posts = post_db.find({"owner" : me})
    more_posts = post_db.find({}).limit(5)
    
    
    if os.path.exists("static/images/" + me2 +"/" + me2 +".jpg"):
        prof_pic = "static/images/" + me2 +"/" + me2 +".jpg" 
      
    else:
        prof_pic = "/static/images/default.jpg"
    links = []
    links.append(prof_pic)
    dez_name = Markup(prof_pic)
    nnn =   "/static/images/" + me2 +"/" + me2 +".jpg"                
    return render_template('profile.html' , me = me , favs = favs , tags = tags , mine = minez ,
                           more = more_posts , links = links , prof = dez_name , nn = nnn)
@application.route('/saved/' , methods = ['POST','GET'])
@login_required
def saved():
    de_render = []
    user_email = session['login_user']
    the_user = users.find_one({"email" :user_email})
    favss = the_user['saved']
    if len(favss) < 1:
        m = "You Dont Have Saved Items"
    else:
        m = " These Are Your Saved Items"
    n = ""
    if n in favss:
        favss.remove(n)
        users.find_one_and_update({'email' : user_email} , {'$set' :  {'saved':favss}})

    for x in favss:
        the_post = post_db.find_one({"post_id" :x})
        de_render.append(the_post)
    if request.method == "POST":
        the_id = request.form['id']
        if request.form['sub'] == "View Link": 
            session["linky"] = the_id
            return redirect(url_for('view_link' ))
        
        if request.form['sub'] == "Remove":
            the_id = request.form['id']
            favss.remove(the_id)
            users.find_one_and_update({'email' : user_email} , {'$set' :  {'saved':favss}})

    return render_template('saved.html' , favss = de_render , m = m )

@application.route('/view_prof/' , methods = ['POST','GET'])
@login_required
def view_prof():
    user = session['de_email']
    user_email = session['login_user']
    the_user = users.find_one({"email" :user})
    mez = users.find_one({'email': user_email})
    folloin = mez['favs']
    all_em_posts = post_db.find({'owner' : user})
    cl = session['login_user']
    folloinx = users.find_one({'email' :cl})
    f = folloinx['favs']
    
    dudes = session["de_email"]
    if not dudes in f:
        state = "Unfollow"
    else:
        state = "Follow"
    
    me = user
    me2 = me.replace("." , "")
    
    if os.path.exists("static/images/" + me2 +"/" + me2 +".jpg"):
        prof_pic = "static/images/" + me2 +"/" + me2 +".jpg" 
      
    else:
        prof_pic = "/static/images/default.jpg"
    links = []
    links.append(prof_pic)
    dez_name = Markup(prof_pic)
    nnn =   "/static/images/" + me2 +"/" + me2 +".jpg" 
    
    if request.method == "POST":
        if request.form['sub'] == "Follow":
            em = []
            the_id = request.form['id']
            if not the_id in f:
                f.append(the_id)
                state = "Unfollow"
                users.find_one_and_update({'email' : user_email} , {'set' : {'favs' : f}})
                return render_template('view_prof.html' , usr = the_user, state = state, pic = nnn , posts = all_em_posts)
            else:
                f.remove(the_id)
                state = "Follow"
                users.find_one_and_update({'email' : user_email} , {'set' : {'favs' : f}})
                return render_template('view_prof.html' , usr = the_user, pic = nnn , state = state , posts = all_em_posts)
                
 
    return render_template('view_prof.html' , usr = the_user, state = state , pic = nnn , posts = all_em_posts)

@application.route('/edit_profile/' ,methods = ['POST','GET'])
@login_required
def edit_profile():
    user = mongo.db.users
    user_email = session['login_user']
    info = user.find({"email" : user_email})
    if request.method == "POST":
        name = request.form['username']
    return render_template('edit_profile.html' , inf = info)

@application.route('/post_on_tags/' , methods = ['POST','GET'])
@login_required
def post_on_tags():
    tag = session['le']
    return render_template('post_on_tags.html')

@application.route('/post/' , methods = ['POST','GET'])
@login_required
def post(): 
    if request.method == "POST":
        post_db = mongo.db.cleos
          
        cleo = request.form['cl'] 
        
        post_id = md5_crypt.hash(cleo)
        
        tag1 = request.form['tag1']
        
        tag2 = request.form['tag2']

        tag_arr = []
        
        tag_arr.append(tag1)
        tag_arr.append(tag2)
        
        owner = session['login_user']
        de_p = owner.replace(".", "")
        pic = "/static/images/"+de_p+"/"+de_p+".jpg"
        wner_name = users.find_one({'email' : owner})
        owner_name = wner_name['username']
        like_arr = [owner]
        comments = []
        post_db.insert_one({"owner" : owner , "likes" : like_arr , "comments" : comments , "cleo" : cleo,
                            "tags" : tag_arr ,  "post_id" : post_id , 'owner_name' : owner_name , "img": pic})
        
        return redirect(url_for('feed'))
    return render_template('post.html')


@application.route('/edit_post/' ,methods = ['POST','GET'])
@login_required
def edit_post():
    da_id = session['post_edit']
    the_post = post_db.find_one({"post_id" : da_id})
    if request.method == "POST":
        de_link = request.form['link']
        de_ttle = request.form['title']
        de_desc = request.form['desc']
        de_tags = request.form['tags']
        link = the_post['link']
        title = the_post['title']
        desc= the_post['description']
        if not de_link  == "":
            link = de_link
        if not de_ttle =="":
            title = de_ttle
        if not de_desc =="":
            desc = de_desc
        if not de_tags =="":
            tags = de_tags
            tags = tags.split(",")
            post_db.find_one_and_update({"post_id" : da_id } , { '$set' :  {"link" : link ,"title" : title , "description" : desc, "tags" : tags}})  
            return redirect(url_for('my_post'))
    return render_template('edit_post.html' , post = the_post)
 
@application.route('/new_main/' , methods = ['POST' , 'GET'])
def new_main():
    if request.method == "POST":
        dt = request.get_json()
        name = dt["name"]
        age = dt["age"]
        
        if name  == "john":
            return render_template("newmain.html" , name = name) 

    return render_template("newmain.html")




@application.route('/my_post/' , methods = ['POST','GET'])
@login_required
def my_post():
    me =  session['login_user']
    me2 = me.replace("." , "")
    thiis_guy = users.find_one({"email" : me})
    this_guy = thiis_guy['username']
    my_posts = post_db.find({"owner" : me})
    tos = []
    for x in my_posts:
        tos.append(x)
    if os.path.exists("static/images/" + me2 +"/" + me2 +".jpg"):
        prof_pic = "static/images/" + me2 +"/" + me2 +".jpg" 
    else:
        prof_pic = "/static/images/default.jpg"
    dez_name = Markup(prof_pic)
    nnn =   "/static/images/" + me2 +"/" + me2 +".jpg" 
    noz = my_posts.count() 
    if request.method == "POST":
        if request.form['sub'] == "Edit":
            id = request.form['the_id']
            session['post_edit'] = id
            return redirect(url_for('edit_post'))
        if request.form['sub'] == "Delete":
            id = request.form['the_id']
            post_db.find_one_and_delete({"post_id" : id})
            return render_template('my_post.html' , posts = tos)
    return render_template('my_post.html' , posts = tos ,no = noz , dude = this_guy , ppic = nnn)


if __name__ == "__main__":
    application.secret_key = "Fuckoffmen"
    application.permanent_session_lifetime = timedelta(days=30)
    application.run(debug = True , port = 5000)

    
