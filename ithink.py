import base64
import shutil
from email import message
from dns.message import Message
from flask import Flask, render_template, url_for, request, redirect,flash,session
from flask.scaffold import F
from flask_pymongo import PyMongo
from flask_wtf.form import FlaskForm
from pymongo import MongoClient
import passlib
from passlib.context import CryptContext
from passlib.hash import bcrypt_sha256,argon2,ldap_salted_md5,md5_crypt
import time
from datetime import timedelta
import smtplib
from email.message import EmailMessage
import socket,os , os.path
from os import path
from functools import wraps
from gridfs import*
from bson import ObjectId
from flask_recaptcha import ReCaptcha
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


ip = socket. gethostbyname(socket. gethostname())
ipst = str(ip)
application = Flask(__name__)


#images
upload_folder = 'static/images'
application.config['UPLOAD_FOLDER'] = upload_folder
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#recaptcha configs
recaptcha = ReCaptcha(application = application)
application.config['RECAPTCHA_PUBLIC_KEY'] =  "6Lf2-MIaAAAAAKhR8vc-wUo6PyWIXtevEN3R7HpY"
application.config['RECAPTCHA_PRIVATE_KEY'] = "6Lf2-MIaAAAAACzF1Nmhmq0dGEGdf9jQJyIqOEmS"
application.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark'}
application.config['TESTING'] = True
#csrf protection
csrf = CSRFProtect(application)
application.config['WTF_CSRF_SECRET_KEY'] = 'edfdfgdfgdfgfghdfggfg'
SECRET_KEY = "dsfdsjgdjgdfgdfgjdkjgdg"
SECRET = "secret"

#mongoDB configs
application.config['MONGO_DBNAME'] = 'users'
# application.config['MONGO_URI'] = 'mongodb://'+ipst+':27017/users'
application.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
mongo = PyMongo(application)


#email configs
application.config['MAIL_SERVER'] = "smtp.gmail.com"
application.config['TESTING'] = True
application.config['MAIL_PORT'] = 465
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_DEBUG'] = True
application.config['MAIL_USERNAME']  = "jacksonmuta123@gmail.com"
application.config['MAIL_PASSWORD'] =  "aqlxhzaziujnllzi"
application.config['MAIL_DEFAULT_SENDER'] = "Service@LinksCustomerCare "
application.config['MAIL_SUpplicationRESS_SEND'] = False
application.config['MAX_EMAIL'] = None
application.config['MAIL_ASCII_ATTATCHMENTS'] = False
service_mail = application.config['MAIL_USERNAME']

Post_guy = Mail(application)

application.permanent_session_lifetime = timedelta(days=30)

Hash_passcode = CryptContext(schemes=["sha256_crypt" ,"argon2" , "bcrypt_sha256"],sha256_crypt__min_rounds=131072)

mongo = PyMongo(application)

users = mongo.db.users
link_db = mongo.db.links

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "login_user" in session:
            return f(*args,**kwargs,)
        else:
            time.sleep(2)
            return redirect(url_for('index'))
    return wrap

def reset_session_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "reset_user" in session:
            return f(*args,**kwargs,)
        else:
            time.sleep(2)
            return redirect(url_for('reset_pass'))
    return wrap



class Base_form(Form):
    
    class Meta:
        csrf = True 
        csrf_class = SessionCSRF 
        csrf_secret = "fhgfjgygkgchfjfjfdumbo"
        csrf_time_limit = timedelta(minutes=25)
        
class login_form(Base_form):
        
        email = StringField("Email",[validators.email()])
        
        passc = PasswordField("Password" , [validators.Length(min = 8 , max = 15 , message = "Minimum Length Is 8 Characters")]) 
          
@application.route('/',methods = ["POST","GET"])
@csrf.exempt
def home():
    form = login_form()
    if request.method == "POST" and form.validate():
        email = form.email.data
        existing_user  = users.find_one({'email':email} )
        if existing_user:
                passcode = form.passc.data

                existing_pass = existing_user['password']
                if Hash_passcode.verify(passcode,existing_pass):
                    username = existing_user['username'] 
                    if username in session:
                        fa = existing_user['tags']
                        if len(fa) < 5:
                             return redirect(url_for('choose_tags'))
                        else:
                            return redirect(url_for('main_page'))
                    else:    
                        session_time = request.form.get("session_time") 
                        if  session_time == 2:
                            session.parmanent = True
                        session['login_user'] = email
                        fa = existing_user['tags']
                        if len(fa) < 5:
                            return redirect(url_for('choose_tags'))
                        else:    
                            return redirect(url_for('main_page'))   
    return render_template("main/middle.html" , form = form)

@application.route('/reset_pass/', methods = ['POST','GET'])
@csrf.exempt
def  reset_pass():
    if request.method == "POST":
        email = request.form['email']
        reset_db = mongo.db.pass_reset
        code = random.randint(145346 , 976578)
        code = str(code)
        existing = users.find_one({'email':email} ) 
        if existing:
            verc = Message(
                "Hello , You Got This Code" + code + "To Verify Your  Account Enter The Following Code To Verify Email" ,
                sender = service_mail ,
                recipients = [email]       
            )
            Post_guy.send(verc)
            r_now = time.time()
            reset_db.insert_one({"email" : email , "code" : code , "time_in" : r_now})
            session['reset_user'] = email
            return redirect(url_for("enter_code"))    
        else:
            return redirect(url_for('register'))
    return render_template('auth/reset_pass.html')

@application.route('/enter_code/' , methods = ['POST','GET'])
@csrf.exempt
@reset_session_required
def enter_code():
    email = session['reset_user']
    if request.method == "POST":
        reset_db = mongo.db.reset_pass
        code = request.form['code']
        mailed = email
        legit = reset_db.find_one({"email" : email})
        if legit:
            legit_code = legit["code"]
            now = time.time()
            req_time = legit['time_in']
            diff = now - req_time
            if code == legit_code and diff < 10:
                  return redirect(url_for('new_pass' , email = mailed))
                
            if diff > 10:
                return redirect(url_for('reset_pass' ))
        else:
            return redirect(url_for('register'))
        
    return render_template('auth/enter_code.html')

class New_pass(Base_form):
      
        pass1 = PasswordField("Password" , [validators.Length(min = 8 , max = 15 , message = "Minimum Length Is 8 Characters")]) 
           
        pass2 = PasswordField("Confirm Password" , [validators.Length(min = 8,max=15 , message=" Minimum Length Is 8 Characters") , EqualTo("passc",message="Must Be Same To The Input Above") , InputRequired()])
        
        

@application.route('/new_pass/' , methods = ['POST','GET'])
@csrf.exempt
def new_pass(email):
    form = New_pass()
    if request.method == "POST" and form.validate():
        users = mongo.db.users
        
        target_account = email
        
        
        pass1 = form.pass1.data
        
        pass2 = form.pass2.data
        
        
        if pass1 == pass2 and len(pass2) > 8 and len(pass2) < 15 :
            
            passcode = Hash_passcode.hash(pass2)
            
            the_user = users.find_one({"email" : email})
             
            users.find_one_and_update({"email" :target_account} , { 'set' : {"password" : passcode} })
    return render_template('new_pass.html' , form = form)








    
if __name__ == "__main__":
    application.secret_key = "Fuckoffmen"
    application.run(debug = True , port = 5003)