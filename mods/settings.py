
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_pymongo import PyMongo

#from flask_mail import Mail,Message
application = Flask(__name__)

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
#Post_guy = Mail(application)

#images
upload_folder = 'static/images'
application.config['UPLOAD_FOLDER'] = upload_folder
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


'''
#recaptcha configs
application.config['RECAPTCHA_PUBLIC_KEY'] =  "6Lf2-MIaAAAAAKhR8vc-wUo6PyWIXtevEN3R7HpY"
application.config['RECAPTCHA_PRIVATE_KEY'] = "6Lf2-MIaAAAAACzF1Nmhmq0dGEGdf9jQJyIqOEmS"
application.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark'}
application.config['TESTING'] = True
recaptcha = ReCaptcha(application = application)

#hcaptcha
application.config['HCAPTCHA_ENABLED'] =  False
application.config ["HCAPTCHA_SITE_KEY"]  =  "cd654ebc-97ad-44fb-8ddc-963287c6d77b"
application.config ['HCAPTCHA_SECRET_KEY'] = "0xb1E280895395797DCF11D0B1807aa9678A4B391d" 
hcaptcha = hCaptcha(application)
'''
#csrf protection
application.config['WTF_CSRF_SECRET_KEY'] = 'edfdfgdfgdfgfghdfggfg'
SECRET_KEY = "dsfdsjgdjgdfgdfgjdkjgdg"
SECRET = "secret"
csrf = CSRFProtect(application)

#mongoDB configs
application.config['MONGO_DBNAME'] = 'users'

# application.config['MONGO_URI'] = 'mongodb://'+ipst+':27017/users'
application.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
mongo = PyMongo(application)

#paypal settings


