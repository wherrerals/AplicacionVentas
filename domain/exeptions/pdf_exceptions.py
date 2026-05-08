class MiddlewareTimeoutError(Exception):
    """El middleware no respondió a tiempo."""


class MiddlewareConnectionError(Exception):
    """No se pudo establecer conexión con el middleware."""


class MiddlewareHTTPError(Exception):
    """El middleware devolvió un código HTTP de error."""
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        super().__init__(message or f"HTTP {status_code} desde el middleware")


class ProductoNotFoundError(Exception):
    """La respuesta del middleware no contiene el campo 'producto'."""