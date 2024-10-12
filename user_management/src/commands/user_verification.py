from .base_command import BaseCommannd
import requests
import os
from ..errors.errors import IncompleteParams, ExternalError
import uuid

class UserVerification(BaseCommannd):
  def __init__(self, data, userId):
    self.data = data
    self.userId = userId
  
  def execute(self):
    response = requests.post(
      f"{self.truenative_host()}/native/verify",
      json=self.truenative_body(),
      headers=self.truenative_headers()
    )
    if response.status_code == 201:
      return response.json()
    else:
      raise ExternalError(response)

  def truenative_host(self):
    return os.getenv('TRUENATIVE_PATH', 'http://localhost:3000')
  
  def secret_token(self):
    return os.getenv('SECRET_TOKEN', 'token')
  
  def webhook_host(self):
    return os.getenv('WEBHOOK_HOST', 'http://localhost:3000')
  
  def truenative_headers(self):
    return {
      'Authorization': f"Bearer {self.secret_token()}"
    }

  def truenative_body(self):
    try:
      return {
        'user': {
          'email': self.data['email'],
          'dni': self.data['dni'],
          'fullName': self.data['fullName'],
          'phone': self.data['phoneNumber'],
        },
        'transactionIdentifier': str(uuid.uuid4()),
        'userIdentifier': self.userId,
        'userWebhook': f'{self.webhook_host()}/users/hook'
      }
    except KeyError:
      raise IncompleteParams()
    except TypeError:
      raise IncompleteParams()