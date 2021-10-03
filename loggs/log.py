import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# New Logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# New Handlers
console_handler = logging.StreamHandler()
info_console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('pnt_logs.log')

# Set the severity level for each handler.
console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)
info_console_handler.setLevel(logging.INFO)

# New Formatter
console_formatter = CustomFormatter()
info_console_formatter = CustomFormatter()
file_formatter = CustomFormatter()

# Set formatters to handlers
console_handler.setFormatter(console_formatter)
info_console_handler.setFormatter(info_console_formatter)
file_handler.setFormatter(file_formatter)

# Add handler to logger.
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(info_console_handler)
