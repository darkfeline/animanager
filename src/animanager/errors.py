class Error(Exception):
    """Animanager error."""


class DBError(Error):
    """Database error."""


class APIError(Error):
    """API error."""
