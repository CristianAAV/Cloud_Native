from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ExternalError
import requests
import os

class TokenAuthentication(BaseCommannd):
  def __init__(self, token):
    self.token = token

  def execute(self):
    host = os.environ['USERS_PATH']
    response = requests.get(
      f'{host}/users/me',
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return True
    else:
      raise ExternalError(response.status_code)