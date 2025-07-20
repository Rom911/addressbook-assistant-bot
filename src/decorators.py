from functools import wraps

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return f"{func.__name__}: Not enough arguments."
        except KeyError:
            return f"{func.__name__}: Key not found."
        except ValueError as ve:
            return f"{func.__name__}: Invalid value. {ve}"
        except Exception as e:
            return f"{func.__name__}: Unexpected error. {e}"
    return wrapper
