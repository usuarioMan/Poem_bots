from json import JSONDecodeError

from logger import logger


class ExtractionError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HeaderExtractionError(ExtractionError):
    """Exception raised for errors while extracting Headers.

    Attributes:
        expression -- expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.header = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        logger.error(f'{self.header} ==> {self.message}')
        pass


class ScrapInmueblesError(ExtractionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        logger.error(f'ERROR SACANDO LA INFORMACIÓN DE UN INMUEBLE .... {self.message}')
        pass


class WriteJsonError(ExtractionError):
    """Exception raised for errors while writing a JSON string error.

    Attributes:
        expression -- expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.write = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        logger.error(f'{self.write} ==> {self.message}')
        pass


class NoScriptTag(ExtractionError):
    """Exception raised for errors while extracting script tags.

    Attributes:
        expression -- expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.header = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        logger.error(f'{self.header} ==> {self.message}')
        pass


class FirstDictionaryExtractionError(ExtractionError):
    """Exception raised for errors while extracting the first dictionary while scraping script tag.

    Attributes:
        expression -- expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.header = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        logger.error(f'{self.header} ==> {self.message}')
        pass


class MyJSONDecodeError(JSONDecodeError):
    def __init__(self, msg, doc, pos):
        self.msg = msg
        self.doc = doc
        self.pos = pos

        super().__init__(self.msg, self.doc, self.pos)
