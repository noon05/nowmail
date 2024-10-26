# exceptions.py

class MailServiceError(Exception):
    """Base Ex MailService."""
    pass


class NetworkError(MailServiceError):
    """Net ex ошибок."""
    pass


class APIError(MailServiceError):
    """API ex"""
    pass