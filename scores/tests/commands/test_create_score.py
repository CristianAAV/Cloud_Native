from src.commands.create_score import CreateScore
from src.session import Session, engine
from src.models.model import Base
from src.models.score import Score
from src.errors.errors import IncompleteParams
from datetime import datetime, timedelta
import uuid

class TestCreateScore():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_score(self):
    data = {
      'offerId': str(uuid.uuid4()),
      'utility': 42.8
    }
    score = CreateScore(data).execute()

    assert score['offerId'] == data['offerId']
    assert score['utility'] == data['utility']

  def test_create_score_missing_fields(self):
    data = {
      'utility': 90,
    }
    try:
      score = CreateScore(data).execute()
      assert False
    except IncompleteParams:
      assert len(self.session.query(Score).all()) == 0
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)