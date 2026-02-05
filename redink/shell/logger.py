import logging

def setup_logger(verbosity: int, silent: bool):
    """
    Sets up the logger with the appropriate verbosity level and format.

    Args:
        verbosity (int): The verbosity level (0-3).
        silent (bool): If True, only errors will be logged.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("redink")
    logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to allow all messages

    # Remove existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Determine the logging level based on verbosity and silent flags
    if silent:
        level = logging.ERROR
    else:
        if verbosity >= 3:
            level = logging.DEBUG
        elif verbosity == 2:
            level = logging.INFO
        elif verbosity == 1:
            level = logging.WARNING
        else:
            level = logging.ERROR

    # Create a StreamHandler with the desired format
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"  # Only show the time (hours:minutes:seconds)
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger