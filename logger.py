import logging
from logging.config import dictConfig
import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(module)s][%(funcName)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'verbose',
            'stream': sys.stderr,
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': [
            'stdout',
            'stderr',
        ],
    },
    'loggers': {
        'elt': {
            'level': 'DEBUG',
            'handlers': [
                'stdout',
                'stderr',
            ],
            'propagate': False,
        },
    },
}


dictConfig(LOGGING)
logger = logging.getLogger('elt')
logger.propagate = False