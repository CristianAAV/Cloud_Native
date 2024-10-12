from .base_command import BaseCommannd
from ..models.user import User, UserJsonSchema
from ..session import Session
from ..errors.errors import Unauthorized, NotToken, NotVerified
from datetime import datetime


class GetUser(BaseCommannd):
    def __init__(self, token=None):
        if token == None or token == "":
            raise NotToken()
        else:
            self.token = self.parse_token(token)

    def execute(self):
        session = Session()

        if len(session.query(User).filter_by(token=self.token).all()) <= 0:
            session.close()
            raise Unauthorized()

        user = session.query(User).filter_by(token=self.token).one()
        if user.expireAt < datetime.now():
            session.close()
            raise Unauthorized()
        
        if user.status != User.STATUS['VERIFIED']:
            session.close()
            raise NotVerified()

        schema = UserJsonSchema()
        user = schema.dump(user)
        session.close()

        return user

    def parse_token(self, token):
        return token.split(' ')[1]
