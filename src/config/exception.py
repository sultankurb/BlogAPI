class ApplicationException(Exception):
    """Базовый класс. По умолчанию это 400 Bad Request."""

    def __init__(self, message: str = "Ошибка бизнес-логики"):
        self.message = message
        super().__init__(self.message)


class NotFoundException(ApplicationException):
    """Группа ошибок 404."""

    def __init__(self, message: str = "Сущность не найдена"):
        super().__init__(message)


class ConflictException(ApplicationException):
    """Группа ошибок 409 (Конфликт данных, например дубликат)."""

    def __init__(self, message: str = "Конфликт данных"):
        super().__init__(message)


class ForbiddenException(ApplicationException):
    """Группа ошибок 403 (Нет прав)."""

    def __init__(self, message: str = "Доступ запрещен"):
        super().__init__(message)
