from .base_command import BaseCommannd
from ..models.score import Score, ScoreSchema
from ..session import Session
from ..errors.errors import IncompleteParams

class CreateScore(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      posted_score = ScoreSchema(
        only=('offerId', 'utility')
      ).load(self.data)
      score = Score(**posted_score)
      session = Session()

      session.add(score)
      session.commit()

      new_score = ScoreSchema().dump(score)
      session.close()

      return new_score
    except TypeError:
      raise IncompleteParams()