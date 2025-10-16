"""
Exceções customizadas para a Store API
"""


class BaseStoreException(Exception):
    """Exceção base para todas as exceções da Store"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ProductNotFound(BaseStoreException):
    """Exceção para quando um produto não é encontrado"""

    def __init__(self, product_id: str):
        message = f"Product with ID '{product_id}' not found"
        super().__init__(message, status_code=404)


class ProductInsertionError(BaseStoreException):
    """Exceção para erros na inserção de produtos"""

    def __init__(self, message: str = "Error inserting product"):
        super().__init__(message, status_code=422)


class ProductUpdateError(BaseStoreException):
    """Exceção para erros na atualização de produtos"""

    def __init__(self, message: str = "Error updating product"):
        super().__init__(message, status_code=422)


class InvalidProductId(BaseStoreException):
    """Exceção para IDs de produto inválidos"""

    def __init__(self, product_id: str):
        message = f"Invalid product ID format: '{product_id}'"
        super().__init__(message, status_code=400)


class DatabaseConnectionError(BaseStoreException):
    """Exceção para erros de conexão com o banco"""

    def __init__(self, message: str = "Database connection error"):
        super().__init__(message, status_code=500)
