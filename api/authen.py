from functools import wraps

from flask import (
    g,
    request,
    abort,
)

from utilities import log_exception

def authen_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            ip = request.headers.get("x-forwarded-for", None)
            if ip is None:
                ip = request.remote_addr
            g.ip = ip
        except Exception as e:
            log_exception(e)
            abort(500)
        return f(*args, **kwargs)

    return decorated_function
