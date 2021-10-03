class DbError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FatalError(Exception):
    """
    Error fatal. Nada que se pueda hacer, cambia el código.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'FATAL ERROR ON DB OPERATION:\n {self.message}'


class CursorAllData(DbError):
    """Exception raised at def cursor_all_data().

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'ERROR AT: cursor_all_data() \n {self.message}'
