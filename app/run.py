import logging
import os

import structlog
import uvicorn

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = os.environ.get("JSON_LOGS", default=False) != "False"


def setup_logging():

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys(): # noqa
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if JSON_LOGS is True:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    renderer,
                ],
                "foreign_pre_chain": pre_chain,
            }
        },
        "handlers": {
            "default": {
                "level": LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "plain",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": LOG_LEVEL,
                "propagate": True,
            },
        }
    })

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


if __name__ == "__main__":
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level=LOG_LEVEL,
        ssl_keyfile="/etc/webhook-tls/tls.key",
        ssl_certfile="/etc/webhook-tls/tls.crt",
        ssl_ca_certs="/etc/webhook-tls/ca.crt",
    )

    server = uvicorn.Server(config)

    setup_logging()

    server.run()
