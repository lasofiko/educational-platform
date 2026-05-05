class DomainException(Exception):
    """базовое доменное исключение"""
    status_code = 400
    default_code = 'error'

    def __init__(self, message=None, status_code=None, code=None):
        self.message = message or self.__class__.__doc__ or 'ошибка'
        if status_code is not None:
            self.status_code = status_code
        self.code = code or self.default_code
        super().__init__(self.message)
