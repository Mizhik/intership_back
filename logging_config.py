import logging
from functools import wraps
import asyncio


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    FORMAT = "[%(levelname)s %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t%(message)s\n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    FILENAME = "app.log"

    logging.basicConfig(
        format=FORMAT, datefmt=TIME_FORMAT, level=level, filename=FILENAME
    )

    logger = logging.getLogger(name)
    return logger


def logger_decorator(func):
    @wraps(func)
    def log_and_call(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised an error: {str(e)}")
            raise e

    @wraps(func)
    async def async_log_and_call(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised an error: {str(e)}")
            raise e

    if asyncio.iscoroutinefunction(func):
        return async_log_and_call
    else:
        return log_and_call
