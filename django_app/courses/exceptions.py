from common.exceptions import DomainException


class NotFoundException(DomainException):
    """ресурс не найден"""
    status_code = 404
    default_code = 'not_found'


class ForbiddenException(DomainException):
    """действие запрещено"""
    status_code = 403
    default_code = 'forbidden'


class ValidationException(DomainException):
    """для ошибок валидации"""
    status_code = 400
    default_code = 'validation_error'


class NodeLocked(ForbiddenException):
    """для заблокированной темы"""
    default_code = 'node_locked'

    def __init__(self, node_id, message=None):
        if message is None:
            message = f'Тема {node_id} заблокирована. Сначала выполните предыдущие задания.'
        super().__init__(message, status_code=403)
        self.node_id = node_id


class LessonNotFound(NotFoundException):
    """урок не найден"""
    default_code = 'lesson_not_found'

    def __init__(self, lesson_id, message=None):
        if message is None:
            message = f'Урок {lesson_id} не найден'
        super().__init__(message, status_code=404)
        self.lesson_id = lesson_id


class NodeNotFound(NotFoundException):
    """тема не найдена"""
    default_code = 'node_not_found'

    def __init__(self, node_id, message=None):
        if message is None:
            message = f'Тема {node_id} не найдена'
        super().__init__(message, status_code=404)
        self.node_id = node_id
