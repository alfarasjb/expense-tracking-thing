import logging
from functools import wraps
from typing import Tuple

import requests
import streamlit as st

logger = logging.getLogger(__name__)


def on_http_error(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except requests.exceptions.ConnectionError:
            err_msg = "Request failed. Connection is not found"
            logger.error(err_msg)
            raise requests.exceptions.ConnectionError(err_msg)
        except Exception as e:
            logger.error(f"Request failed. An unknown error occurred. Exception: {e}")
    return wrapper


def authentication(success_msg: str, fail_msg: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[bool, str]:
            try:
                response, name = func(*args, **kwargs)
                success = response
                if success:
                    logger.info(success_msg)
                    # st.success(success_msg)
                else:
                    st.error(fail_msg)
                return success, name
            except requests.exceptions.ConnectionError as e:
                st.error(str(e))
                return False, ""
            except Exception as e:
                logger.error(f"An unknown error occurred: {e}")
                return False, ""
        return wrapper
    return decorator
