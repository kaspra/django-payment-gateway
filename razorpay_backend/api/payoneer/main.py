import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.exceptions import APIException

class PayoneerClient:

  def create_order(self,amount,currency,transactionId,email,street,city,zip,country,firstname,lastname):
    returnUrl = "https://google.com" # place the success run url
    cancelUrl = "https://google.com" # place the cancel url
    notificationUrl = "https://google.com" # place the notification url

    response = requests.post(
      f"{settings.PAYONEER_API_URL}",
      headers={
        'Authorization': f'Bearer {settings.PAYONEER_API_KEY}',
        'Content-Type': 'application/json'
      },
      json={
        "transactionId": transactionId, 
        "integration": "HOSTED",
        "operationType": "CHARGE",
        "division": "LilySilk_HK", # this is a store code get from integration page when we create a store
        "country": country,
        "customer": {
          "email": email,
          "addresses": {
            "billing": {
              "street": street,
              "city": city,
              "zip": zip,
              "country": country,
              "name": {
                "firstName": firstname,
                "lastName": lastname
              }
            },
            "shipping": {
              "street": street,
              "city": city,
              "zip": zip,
              "country": country,
              "name": {
                "firstName": firstname,
                "lastName": lastname
              }
            }
          }
        },
        "payment": {
          "amount": amount,
          "currency": currency,
          "reference": "PM Checkout Example"
        },
        "style": {
          "language": "en_US",
          "hostedVersion": "v4"
        },
        "callback": {
          "returnUrl": returnUrl,
          "cancelUrl": cancelUrl,
          "notificationUrl": notificationUrl
        }
      }

    )

    if response.status_code in [200, 201]:
      return response.json()
    else:
      print("Failed Text",response.text)
      raise APIException(
          {
              "status_code": response.status_code,
              "message": response,
          }
      )

  def verify_payment(self, listId):
    response = requests.get(
      f"{settings.PAYONEER_API_URL}/{listId}",
      headers={
        'Authorization': f'Bearer {settings.PAYONEER_API_KEY}',
        'Content-Type': 'application/json'
      }
    )

    if response.status_code in [200,201]:
      return response.json()
    else:
      print("Verification Failed",response)
      raise APIException(
        {
          "status_code": response.status_code,
          "message": response
        }
      )