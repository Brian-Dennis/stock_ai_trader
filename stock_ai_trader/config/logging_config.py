import logging
import logging.handlers
import os
from datetime import datetime

class LoggingConfig:
    def __init__(self):
        """
        Initialize logging configuration
        """
        # Create logs directory
        self.logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)

        # Create log files paths
        self.trading_log_file = os.path.join(self.logs_dir, 'trading.log')
        self.error_log_file = os.path.join(self.logs_dir, 'error.log')
        self.debug_log_file = os.path.join(self.logs_dir, 'debug.log')

    def setup_logging(self) -> None:
        """
        Configure logging for the application
        """
        # Create formatters
        standard_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
        )

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Trading activity logger
        trading_handler = logging.handlers.RotatingFileHandler(
            self.trading_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        trading_handler.setLevel(logging.INFO)
        trading_handler.setFormatter(standard_formatter)
        
        # Error logger
        error_handler = logging.handlers.RotatingFileHandler(
            self.error_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Debug logger
        debug_handler = logging.handlers.RotatingFileHandler(
            self.debug_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(standard_formatter)

        # Add handlers to root logger
        root_logger.addHandler(trading_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(debug_handler)
        root_logger.addHandler(console_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger with the specified name
        :param name: Name of the logger
        :return: Logger instance
        """
        return logging.getLogger(name)

# Singleton instance
logging_config = LoggingConfig()

def setup_logging():
    """
    Setup logging configuration
    """
    logging_config.setup_logging()

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    :param name: Name of the logger
    :return: Logger instance
    """
    return logging_config.get_logger(name)

if __name__ == "__main__":
    # Example usage
    setup_logging()
    logger = get_logger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

