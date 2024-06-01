"""Custom Logger setup for Backend codebase"""

import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.getLogger().setLevel(log_level)


class BackendLogger:
    """
    Custom logger class that formats log messages as JSON.We can further extend it to include other usefull metrics like unique trace_id per request.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def _format_msg(self, level: int, message: str, **kwargs) -> str:
        """
        Formats the log message as a JSON string with additional context.

        Args:
            level (int): The log level (Ex: logging.INFO).
            message (str): The log message.
            **kwargs: Additional context to include in the log message.

        Returns:
            str: The formatted JSON log message.
        """
        kwargs["timestamp"] = datetime.utcnow().isoformat()
        kwargs["level"] = logging.getLevelName(level)
        kwargs["message"] = message
        return json.dumps(kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """To log info message"""
        self._log(logging.INFO, message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """To log a warning message."""
        self._log(logging.WARNING, message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """To log an error message."""
        self._log(logging.ERROR, message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        """To log a debug message."""
        self._log(logging.DEBUG, message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """To log a critical message."""
        self._log(logging.CRITICAL, message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs) -> None:
        """To log an error message with exception traceback."""
        self._log(logging.ERROR, message, exc_info=True, *args, **kwargs)

    def _log(self, level: int, message: str, *args, **kwargs) -> None:
        """Internal method to handle the actual logging."""
        formatted_message = self._format_msg(level, message, **kwargs)
        self.logger.log(level, formatted_message, *args)


logger: BackendLogger = BackendLogger()
