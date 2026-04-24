class DomainException(Exception):
    """базовое исключение"""
    status_code = 400
    def __init__(self, message, status_code=None):
        self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(DomainException):
    """ресурс не найден"""
    status_code = 404

class ForbiddenException(DomainException):
    """действие запрещено"""
    status_code = 403

class ValidationException(DomainException):
    """для ошибок валидации"""
    status_code = 400
class NodeLocked(ForbiddenException):
    """для заблокированной темы"""
    def __init__(self, node_id, message=None):
        if message is None:
            message = f"Тема {node_id} заблокирована. Сначала выполните предыдущие задания."
        super().__init__(message, status_code=403)
        self.node_id = node_id

class LessonNotFound(NotFoundException):
    """урок не найден"""
    def __init__(self, lesson_id, message=None):
        if message is None:
            message = f"Урок {lesson_id} не найден"
        super().__init__(message, status_code=404)
        self.lesson_id = lesson_id


class NodeNotFound(NotFoundException):
    """исключение для ненайденной темы"""
    def __init__(self, node_id, message=None):
        if message is None:
            message = f"Тема {node_id} не найдена"
        super().__init__(message, status_code=404)
        self.node_id = node_id

class AlreadyEnrolled(DomainException):
    """пользователь уже записан на курс"""
    def __init__(self, message=None, user_id=None, course_id=None):
        if message is None:
            message = "Пользователь уже записан на этот курс"
        super().__init__(message, status_code=400)
        self.user_id = user_id
        self.course_id = course_id