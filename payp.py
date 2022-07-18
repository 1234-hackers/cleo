from flask import Flask, render_template, jsonify, request
import paypalrestsdk

import requests
app = Flask(__name__)


#auth token

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




#update


url = "https://api.sandbox.paypal.com/v2/checkout/orders/5O190127TN364715T"

payload = """[
  {
    \"op\": \"replace\",
    \"path\": \"/purchase_units/@reference_id=='PUHF'/amount\",
    \"value\": {
      \"currency_code\": \"USD\",
      \"value\": \"200.00\",
      \"breakdown\": {
        \"item_total\": {
          \"currency_code\": \"USD\",
          \"value\": \"180.00\"
        },
        \"shipping\": {
          \"currency_code\": \"USD\",
          \"value\": \"20.00\"
        }
      }
    }
  }
]"""
headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'accept-language': "en_US",
    'authorization': "Bearer A21AAFJ9eoorbnbVH3fTJrCTl2o7-P_1T6q8vdYB_QwBB9Ais5ZZmJD4BsNjIiOh8j8OyOcfzLO1BKcgKe0pK-mntpk6jOm-"
    }

response = requests.request("PATCH", url, data=payload, headers=headers)

print(response.status_code)

print(response.text)




#capture

import requests

url = "https://api.sandbox.paypal.com/v2/checkout/orders/5O190127TN364715T/capture"

headers = {
    'content-type': "application/json",
    'authorization': "Bearer A21AAFJ9eoorbnbVH3fTJrCTl2o7-P_1T6q8vdYB_QwBB9Ais5ZZmJD4BsNjIiOh8j8OyOcfzLO1BKcgKe0pK-mntpk6jOm-"
    }

response = requests.request("POST", url, headers=headers)

print(response.status_code)

print(response.text)

if __name__ == '__main__':
    app.run(debug=True , port = 5001)
