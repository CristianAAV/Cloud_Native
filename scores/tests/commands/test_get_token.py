from src.commands.token_authentication import TokenAuthentication
from src.session import Session, engine
from src.models.model import Base
from httmock import HTTMock
from src.errors.errors import ExternalError
from uuid import uuid4
from tests.mocks import mock_failed_auth, mock_success_auth


class TestGetToken():
  def test_authenticate(self):
    with HTTMock(mock_success_auth):
      result = TokenAuthentication(str(uuid4())).execute()
      assert result == True

  def test_failed_authenticate(self):
    with HTTMock(mock_failed_auth):
      try:
        TokenAuthentication(str(uuid4())).execute()
        assert False
      except ExternalError:
        assert True
