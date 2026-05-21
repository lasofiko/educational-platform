class UGCException(Exception):
    """Базовое исключение"""
    def __init__(self, detail, code, http_status=400):
        self.detail = detail
        self.code = code
        self.http_status = http_status
        super().__init__(detail)

class TargetNotFound(UGCException):
    """Урок или предмет не найден в Django"""
    def __init__(self, target_type, target_id):
        super().__init__(detail=f'{target_type} с id {target_id} не найден',code='target_not_found',http_status=404)
class AlreadyReviewed(UGCException):
    """Пользователь уже оставил отзыв"""
    def __init__(self, user_id, target_type, target_id):
        super().__init__(detail=f'Пользователь {user_id} уже оставил отзыв на {target_type} {target_id}',code='already_reviewed',http_status=409)
class UGCNotFound(UGCException):
    """Отзыв или комментарий не найден в БД"""
    def __init__(self, ugc_type, ugc_id):
        super().__init__(detail=f'{ugc_type} с id {ugc_id} не найден',code='ugc_not_found',http_status=404)

class InvalidStatus(UGCException):
    """Неправильный статус"""
    def __init__(self, status):
        super().__init__(detail=f'Неправильный статус: {status}. Допустимые: active, hidden, pending',code='invalid_status',http_status=400)
class DjangoUnavailable(UGCException):
    """Django сервис недоступен (не отвечает на запросы)"""
    def __init__(self):
        super().__init__(detail='Сервис курсов временно недоступен',code='django_unavailable',http_status=503)