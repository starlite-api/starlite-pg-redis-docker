from logging.config import dictConfig


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%H:%M:%S",
                    "format": "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                },
            },
            "loggers": {
                "app": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
                "starlite": {"handlers": ["console"], "level": "INFO", "propagate": True},
                "databases": {"handlers": ["console"], "level": "WARNING"},
            },
        }
    )
