import logging
import time
from typing import Callable, Any, Optional
from functools import wraps
import traceback

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def handle_errors(func):
    ####Menggunakan fungsi wrap
    @wraps(func)
    def wrapper(*arg, **kwargs):
        start_time = time.time()
        try:
            result = func(*arg, **kwargs)
        except Exception as e:
            execution_time = time.time() - start_time
            tb = traceback.extract_tb(e.__traceback__)
            filename, lineno, funcname, text = tb[-1]
            error_message = (
                    f"An error occurred in function {func.__name__} at {filename}:{lineno} - {text}"
            )
            logger.error(f"Function {func.__name__} failed after {execution_time:.4f} seconds with error: {e}")
            logger.error(error_message)
    return wrapper

def complex_handle_errors(loggering=None, log_message: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                if 'nomessagesNormal' in kwargs:
                    nomessagesNormal = kwargs['nomessagesNormal']
                else:
                    nomessagesNormal = False
            except:
                nomessagesNormal = True
            try:
                loggering.info(f"Executing function: {func.__name__} with args: {args} and kwargs: {kwargs}")
                result = func(*args, **kwargs)
                if nomessagesNormal == True:
                    execution_time = time.time() - start_time
                    loggering.info(f"Function {func.__name__} executed successfully in {execution_time:.4f} seconds")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                tb = traceback.extract_tb(e.__traceback__)
                filename, lineno, funcname, text = tb[-1]
                error_message = (
                    log_message or 
                    f"An error occurred in function {func.__name__} at {filename}:{lineno} - {text}"
                )
                loggering.error(f"Function {func.__name__} failed after {execution_time:.4f} seconds with error: {e}")
                loggering.error(error_message)
                return ""  # Atau nilai default sesuai kebutuhan


        return wrapper

    # Check if decorator is used without arguments
    if callable(log_message):
        return decorator(log_message)

    return decorator
