class ApiError(Exception):
    code = 422
    description = "Default message"


class UserAlreadyExists(ApiError):
    code = 412
    description = "User with username or email already exists"


class UserNotFoundError(ApiError):
    code = 404
    description = "User with username and password does not exist"


class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"


class NotToken(ApiError):
    code = 403
    description = "You need to specify a auth token"


class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"

class NotVerified(ApiError):
    code = 401
    description = "User is not verified"

class ExternalError(ApiError):
    DEFAULT_MESSAGE = "External error"

    code = 422  # Default
    description = DEFAULT_MESSAGE

    def __init__(self, response):
        self.code = response.status_code
        message = self.message_from_response(response)
        if message:
            self.description = message

    def message_from_response(self, response):
        try:
            json = response.json()
            if 'msg' in json:
                return json['msg']
        except:
            ...
        return None
