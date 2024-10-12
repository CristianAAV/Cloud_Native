from .base_command import BaseCommannd
from ..models.user import User, UserJsonSchema
from ..session import Session
from ..errors.errors import UserNotFoundError, IncompleteParams

class UpdateScore(BaseCommannd):
  MIN_SCORE = 60

  def __init__(self, id, score):
    if id == "":
      raise IncompleteParams()
    self.id = id
    self.score = score
  
  def execute(self):
    session = Session()
    
    if len(session.query(User).filter_by(id=self.id).all()) <= 0:
      session.close()
      raise UserNotFoundError()

    status = User.STATUS['VERIFIED'] if self.score >= self.MIN_SCORE else User.STATUS['NOT_VERIFIED']

    user = session.query(User).filter_by(id=self.id).one()
    user.score = self.score
    user.status = status
    session.commit()

    schema = UserJsonSchema()
    user = schema.dump(user)
    session.close()
    return user