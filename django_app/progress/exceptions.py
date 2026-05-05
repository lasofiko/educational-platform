from django_app.common.exceptions import DomainExceptions

class AlreadyEnrolled(DomainExceptions):
    default_detail = "Студент уже записан на курс"
    default_code = "already_enrolled"
    status_code = 409

class NotEnrolled(DomainExceptions):
    default_detail = "Студент не записан на курс"
    default_code = "not_enrolled"

class QuizFailed(DomainExceptions):
    default_detail = "Тест не пройден (результат менее 70%)"
    default_code = "quiz_failed"

class InvalidAnswer(DomainExceptions):
    default_detail = "Неправильный ответ"
    default_code = "invalid_answer"

class SubjectNotFound(DomainExceptions):
    default_detail = "Указанный предмет не существует"
    default_code = "subject_not_found"