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
from mods.settings import csrf,Post_guy,upload_folder,recaptcha,mongo,hcaptcha

from mods.datas import tech,enta,sports,rel_life_stylem,buss_invest,tags1

from mods.methods import login_required,sendMail_trap,sendGmail,reset_session_required,get_the_token,capture_pyp,create_order

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
 
from mods.routes import  home,reset_pass,enter_code,login,logout,register,choose_tags,choose_favs,feed,profile,saved,view_prof,edit_profile,post_on_tag,view_link,post_edit_post,new_main
         
@application.route('/',methods = ["POST","GET"])
home()


@application.route('/reset_pass/', methods = ['POST','GET'])
reset_pass()


@application.route('/enter_code/' , methods = ['POST','GET'])
enter_code()

                
@application.route('/login/' , methods = ['POST','GET'])
login()

@application.route('/logout/' , methods = ['POST','GET'])
@login_required
logout()

@application.route('/register/',methods = ['POST','GET'])
register()

    
@application.route('/choose_tags/' , methods = ['POST','GET'])
@login_required
choose_favs()

@application.route('/choose_favs/' , methods = ['POST','GET'])
@login_required
choose_favs()

@application.route('/feed/' , methods = ['POST','GET'])
@login_required
feed()


@application.route('/profile/' , methods = ['POST','GET'])  
@login_required
profile()

@application.route('/saved/' , methods = ['POST','GET'])
@login_required
saved()

@application.route('/view_prof/' , methods = ['POST','GET'])
@login_required
view_prof()

@application.route('/edit_profile/' ,methods = ['POST','GET'])
@login_required
edit_profile()

@application.route('/post_on_tags/' , methods = ['POST','GET'])
@login_required
post_on_tags()

@application.route('/post/' , methods = ['POST','GET'])
@login_required
post()

@application.route('/edit_post/' ,methods = ['POST','GET'])
@login_required
edit_post()
    
@application.route('/new_main/' , methods = ['POST' , 'GET'])
new_main()

@application.route('/my_post/' , methods = ['POST','GET'])
@login_required
my_post()


if __name__ == "__main__":
    application.secret_key = "Fuckoffmen"
    application.permanent_session_lifetime = timedelta(days=30)
    application.run(debug = True , port = 5000)

    
