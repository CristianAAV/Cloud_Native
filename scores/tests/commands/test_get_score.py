from src.commands.get_score import GetScore
from src.commands.create_score import CreateScore
from src.session import Session, engine
from src.models.model import Base
from src.models.score import Score
from src.errors.errors import InvalidParams, ScoreNotFoundError
import uuid
from tests.utils.constants import STATIC_FAKE_UUID

class TestGetScoreOfoffer():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    self.data = {
      'offerId': str(uuid.uuid4()),
      'utility': 50.2
    }
    self.score = CreateScore(self.data).execute()

  def test_get_score_of_offer(self):
    score = GetScore(self.score['offerId']).execute()

    assert score['id'] == self.score['id']
    assert score['offerId'] == self.score['offerId']
    assert score['utility'] == self.score['utility']

  def test_get_score_invalid_offer_id(self):
    try:
      GetScore('non_number_id').execute()

      assert False
    except InvalidParams:
      assert True

  def test_get_score_of_offer_doesnt_exist(self):
    try:
      GetScore(STATIC_FAKE_UUID).execute()

      assert False
    except ScoreNotFoundError:
      assert True

  
  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)