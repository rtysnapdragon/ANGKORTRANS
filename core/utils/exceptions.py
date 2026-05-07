from rest_framework.exceptions import APIException

class JWTExpiredException(APIException):
    status_code = 401
    default_detail = 'JWT token was expired-------'
    default_code = 'token_expired'

    # def __init__(self):
    #     self.detail = {
    #         "Message": {default_detail},
    #         "Code": "token_expired"
    #     }

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.detail = {
            "Message": self.default_detail,
            "StatusCode": self.status_code,
            "ErrorCode": self.default_code
        }

class JWTInvalidException(APIException):
    status_code = 403
    default_detail = 'Invalid JWT token'
    default_code = 'invalid_token'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.detail = {
            "Message": self.default_detail,
            "StatusCode": self.status_code,
            "ErrorCode": self.default_code
        }