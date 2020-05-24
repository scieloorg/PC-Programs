
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'brief': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'brief',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'prodtools.log',
            'maxBytes': 10240,
            'backupCount': 3,
        },
        'file2': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'prodtools.err',
            'maxBytes': 10240,
            'backupCount': 3,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file', 'file2', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
