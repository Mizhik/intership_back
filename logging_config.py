import logging
from functools import wraps
import asyncio
from typing import Any
from pydantic import BaseModel
from datetime import datetime

from app.entity.models import User


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    FORMAT = "[%(levelname)s %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t%(message)s\n"
    TIME_FORMAT = "%d.%м.%Y %I:%M:%S %p"

    FILENAME = "app.log"

    logging.basicConfig(
        format=FORMAT, datefmt=TIME_FORMAT, level=level, filename=FILENAME
    )

    logger = logging.getLogger(name)
    return logger


def redact_sensitive_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            k: "***" if k == "password" else redact_sensitive_data(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]
    elif hasattr(data, "__dict__"):
        data_dict = {
            k: v for k, v in data.__dict__.items() if k != "_sa_instance_state"
        }
        if "password" in data_dict:
            data_dict["password"] = "***"
        if "create_at" in data_dict and isinstance(data_dict["create_at"], datetime):
            data_dict["create_at"] = data_dict["create_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        if "update_at" in data_dict and isinstance(data_dict["update_at"], datetime):
            data_dict["update_at"] = data_dict["update_at"].strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        return data_dict
    elif isinstance(data, BaseModel):  # Обработка Pydantic моделей
        data_dict = data.dict()
        if "password" in data_dict:
            data_dict["password"] = "***"
        return data_dict
    else:
        return data


def process_args(*args, **kwargs):
    filtered_args = [redact_sensitive_data(arg) for arg in args]
    filtered_kwargs = {k: redact_sensitive_data(v) for k, v in kwargs.items()}
    return filtered_args, filtered_kwargs


def logger_decorator(func):
    @wraps(func)
    def log_and_call(*args, **kwargs):
        logger = get_logger(func.__module__)
        filtered_args, filtered_kwargs = process_args(*args, **kwargs)
        logger.info(
            f"Calling {func.__name__} with args: {repr(filtered_args)}, kwargs: {repr(filtered_kwargs)}"
        )
        try:
            result = func(*args, **kwargs)
            filtered_result = redact_sensitive_data(result)
            logger.info(f"{func.__name__} returned: {repr(filtered_result)}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised an error: {str(e)}")
            raise e

    @wraps(func)
    async def async_log_and_call(*args, **kwargs):
        logger = get_logger(func.__module__)
        filtered_args, filtered_kwargs = process_args(*args, **kwargs)
        logger.info(
            f"Calling {func.__name__} with args: {repr(filtered_args)}, kwargs: {repr(filtered_kwargs)}"
        )
        try:
            result = await func(*args, **kwargs)
            filtered_result = redact_sensitive_data(result)
            logger.info(f"{func.__name__} returned: {repr(filtered_result)}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised an error: {str(e)}")
            raise e

    if asyncio.iscoroutinefunction(func):
        return async_log_and_call
    else:
        return log_and_call
