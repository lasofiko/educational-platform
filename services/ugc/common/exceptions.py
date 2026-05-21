class UGCException(Exception):

    status_code = 400
    default_code = 'ugc_error'

    def __init__(self, message=None, status_code=None, code=None):
        self.message = message or self.__class__.__doc__ or 'ошибка'
        if status_code is not None:
            self.status_code = status_code
        self.code = code or self.default_code
        super().__init__(self.message)


class DuplicateReviewError(UGCException):
    status_code = 409
    default_code = 'duplicate_review'


class TargetNotFoundError(UGCException):

    status_code = 404
    default_code = 'target_not_found'


class UGCNotFoundError(UGCException):

    status_code = 404
    default_code = 'not_found'


class UnauthorizedError(UGCException):

    status_code = 401
    default_code = 'unauthorized'


class ForbiddenError(UGCException):

    status_code = 403
    default_code = 'forbidden'
