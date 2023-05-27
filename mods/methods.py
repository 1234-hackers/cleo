'''
    This files contains any functions used in the API
'''

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "login_user" in session:
            return f(*args,**kwargs,)
        else:
            time.sleep(2)
            return redirect(url_for('home'))
    return wrap


#session stored during password reset
def reset_session_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "login_user" in session:
            return f(*args,**kwargs,)
        else:
            time.sleep(2)
            return redirect(url_for('reset_pass'))
    return wrap



#send email using gmail
def sendGmail(sender,recipients,mess):
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = "jacksonmuta123@gmail.com"
    app.config['MAIL_PASSWORD'] =  "aqlxhzaziujnllzi"
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail = Mail(app)

    msg = Message('Hello from the other side!', sender =   sender, recipients = recipients)
    msg.body = mess
    mail.send(msg)
    
    
def sendMail_trap(sender,recipients):
    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'dcf92fb9c62985'
    app.config['MAIL_PASSWORD'] = '68368278225bba'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail = Mail(app)
    
    msg = Message('Hello from the other side!', sender =   sender, recipients = recipients)
    msg.body = mess
    mail.send(msg)
    
    
#paypal based functions

#auth token
def get_the_token():
    paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or live
    "client_id": "AcCtp81-85dHxl5Q6WRJXddA0NOIZfJV94JXupG_-SxH3hu9nudUyWmsBuIKCSuLKj9lmFQc6FWQiJrt",
    "client_secret": "EJMzvx11evGV7TnYHtFor0JcRrMjk31xr1fxOoWZDqyTxTPaHEXXjl4Rt8I7W8TTuoBoH4_csQtpgQ09"
    })
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    payload = "grant_type=client_credentials"
    headers = {
        'accept': "application/json",
        'accept-language': "en_US",
        'content-type': "application/x-www-form-urlencoded",
        'authorization': "basic QWYt**********MGc="
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)
    print(response.text)


#capture function
def capture_pyp():
    url = "https://api.sandbox.paypal.com/v2/checkout/orders/5O190127TN364715T/capture"
    headers = {
      'content-type': "application/json",
      'authorization': "Bearer A21AAFJ9eoorbnbVH3fTJrCTl2o7-P_1T6q8vdYB_QwBB9Ais5ZZmJD4BsNjIiOh8j8OyOcfzLO1BKcgKe0pK-mntpk6jOm-"
      }
    response = requests.request("POST", url, headers=headers)
    print(response.status_code)
    print(response.text)
    
#create order
def create_order():
  url = "https://api.sandbox.paypal.com/v2/checkout/orders"
  payload = """{
    \"intent\": \"CAPTURE\",
    \"purchase_units\": [
      {
        \"reference_id\": \"PUHF\",
        \"amount\": {
          \"currency_code\": \"USD\",
          \"value\": \"100.00\"
        }
      }
    ],
    \"application_context\": {
      \"return_url\": \"\",
      \"cancel_url\": \"\"
    }
  }"""
  headers = {
      'accept': "application/json",
      'content-type': "application/json",
      'accept-language': "en_US",
      'authorization': "Bearer A21AAFJ9eoorbnbVH3fTJrCTl2o7-P_1T6q8vdYB_QwBB9Ais5ZZmJD4BsNjIiOh8j8OyOcfzLO1BKcgKe0pK-mntpk6jOm-"
      }

  response = requests.request("POST", url, data=payload, headers=headers)

  print(response.status_code)

  print(response.text)
    

 