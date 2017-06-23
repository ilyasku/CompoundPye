LOGGER_CONFIG_DICT = {
    "version": 1,
    "formatters":
    {
        "simple":
        {
            "format": '%(levelname)s:%(name)s: %(message)s'
        }
    },    
    "handlers":
    {
        "console":
        {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers":
    {        
        "CompoundPye":
        {
            "level": "WARNING",
            "handlers": ["console"],            
            "propagate": False
        }
    },
    "root":
    {
        "level": "WARNING",
        "handlers": ["console"]
    }
}
