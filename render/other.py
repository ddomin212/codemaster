from functools import wraps
from random import choice

import streamlit as st

ERROR_ICONS = ["⚠️", "🚫", "🛑", "🔥", "🤯", "🤬", "👺", "👹", "👿", "💀", "☠️"]


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(body=e, icon=choice(ERROR_ICONS))

    return wrapper
