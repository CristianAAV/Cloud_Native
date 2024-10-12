from .base_command import BaseCommannd
from ..models.score import Score, ScoreSchema
from ..session import Session
from ..errors.errors import InvalidParams, ScoreNotFoundError

class GetScore(BaseCommannd):
  def __init__(self, offer_id):
    if self.is_uuid(offer_id):
      self.offer_id = offer_id
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(Score).filter_by(offerId=self.offer_id).all()) <= 0:
      session.close()
      raise ScoreNotFoundError()

    score = session.query(Score).filter_by(offerId=self.offer_id).all()[0]
    schema = ScoreSchema()
    score = schema.dump(score)
    session.close()
    return score
