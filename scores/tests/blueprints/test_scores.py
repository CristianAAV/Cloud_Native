from src.session import Session, engine
from src.models.model import Base
from src.models.score import Score
from src.main import app
import json
from uuid import uuid4
from src.commands.create_score import CreateScore
from tests.mocks import mock_failed_auth, mock_success_auth, mock_forbidden_auth
from httmock import HTTMock
import uuid
from tests.utils.constants import STATIC_FAKE_UUID

class Testoffers():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_score(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/scores', json={
            'offerId': str(uuid.uuid4()),
            'utility': 100.2
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'offerId' in response_json
        assert 'utility' in response_json
  
  def test_create_score_invalid_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/scores', json={
            'offerId': str(uuid.uuid4()),
            'utility': 100.2
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )

        assert response.status_code == 401

  def test_create_score_without_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.post(
          '/scores', json={
            'offerId': str(uuid.uuid4()),
            'utility': 100.2
          }
        )

        assert response.status_code == 403

  def test_create_score_missing_fields(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/scores', json={
            'offerId': str(uuid.uuid4()),
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 400

  def test_get_score_of_offer(self):
    data = {
      'offerId': str(uuid.uuid4()),
      'utility': 100.2
    }
    score = CreateScore(data).execute()
  
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/scores/offer/{score["offerId"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'offerId' in response_json
        assert 'utility' in response_json

  def test_get_score_of_offer_invalid_token(self):
    data = {
      'offerId': str(uuid.uuid4()),
      'utility': 100.2
    }
    score = CreateScore(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/scores/offer/{score["offerId"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )

        assert response.status_code == 401

  def test_get_score_of_offer_without_token(self):
    data = {
      'offerId': str(uuid.uuid4()),
      'utility': 100.2
    }
    score = CreateScore(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          f'/scores/offer/{score["offerId"]}'
        )

        assert response.status_code == 403

  def test_get_score_of_offer_invalid_id(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/scores/offer/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 400

  def test_get_score_of_offer_doesnt_exist(self):
    data = {
      'offerId': str(uuid.uuid4()),
      'utility': 100.2
    }
    score = CreateScore(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/scores/offer/{STATIC_FAKE_UUID}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 404

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get(
        '/scores/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/scores/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)