import logging
import os
Logger=None
def configure_logging(log_file_path="log/app.log"):
    """Configures logging based on environment variable LOG_LEVEL."""
    if Logger == None:
        # Get log level from environment variable, defaulting to INFO
        log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()

        try:
            log_level = getattr(logging, log_level_str)
        except AttributeError:
            print(f"Invalid log level '{log_level_str}' specified. Using INFO.")
            
            log_level = logging.INFO
            
        
        logger=logging.getLogger(__name__)
        logger.setLevel(level=log_level)
        if len(logger.handlers) ==0:
            logger.addHandler(logging.FileHandler(log_file_path))
            logger.addHandler(logging.StreamHandler())
          
            # set the format
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
            for handler in logger.handlers:
                handler.setFormatter(formatter)
    return logger





