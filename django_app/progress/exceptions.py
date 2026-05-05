from common.exceptions import DomainException
from courses.exceptions import NotFoundException


class AlreadyEnrolled(DomainException):
    """пользователь уже записан на курс"""
    status_code = 409
    default_code = 'already_enrolled'

    def __init__(self, message=None, user_id=None, course_id=None, **kw):
        super().__init__(message or 'Студент уже записан на курс', **kw)
        self.user_id = user_id
        self.course_id = course_id


class NotEnrolled(DomainException):
    """пользователь не записан на курс"""
    status_code = 404
    default_code = 'not_enrolled'

    def __init__(self, message=None, **kw):
        super().__init__(message or 'Студент не записан на курс', **kw)


class SubjectNotFound(NotFoundException):
    """предмет не найден"""
    default_code = 'subject_not_found'

    def __init__(self, message=None, **kw):
        super().__init__(message or 'Указанный предмет не существует', **kw)


class ProblemNotFound(NotFoundException):
    """задача не найдена"""
    default_code = 'problem_not_found'

    def __init__(self, problem_id=None, message=None, **kw):
        super().__init__(message or f'Задача {problem_id} не найдена', **kw)
        self.problem_id = problem_id


class QuizNotFound(NotFoundException):
    """тест не найден"""
    default_code = 'quiz_not_found'

    def __init__(self, quiz_id=None, message=None, **kw):
        super().__init__(message or f'Тест {quiz_id} не найден', **kw)
        self.quiz_id = quiz_id


class QuizFailed(DomainException):
    """тест не пройден"""
    status_code = 400
    default_code = 'quiz_failed'

    def __init__(self, message=None, **kw):
        super().__init__(message or 'Тест не пройден (результат менее 70%)', **kw)


class InvalidAnswer(DomainException):
    """неправильный ответ"""
    status_code = 400
    default_code = 'invalid_answer'

    def __init__(self, message=None, **kw):
        super().__init__(message or 'Неправильный ответ', **kw)
