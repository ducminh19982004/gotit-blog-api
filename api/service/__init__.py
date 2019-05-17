from flask import (
    jsonify,
    make_response,
    request,
)

from api import (
    app,
    logger,
)


@app.before_request
def before():
    ip = request.headers.get("x-forwarded-for", None)
    if ip is None:
        ip = request.remote_addr
    data_input = {
        'ip': ip,
        'url': request.url,
        'method': request.method,
        'content': request.data,
        'stream': request.stream,
        'headers': {},
    }
    logger.info('Input: \n%s', data_input)


@app.after_request
def after(response):
    try:
        logger.info('Output: %s', response.get_data())
    except:
        pass
    return response


@app.errorhandler(400)
def bad_request(error):
    return make_response('Bad Request', 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response('Unauthorized', 401)


@app.errorhandler(404)
def not_found(error):
    return make_response('Not Found', 404)


@app.errorhandler(410)
def gone(error):
    return make_response('Gone', 410)


@app.errorhandler(415)
def gone(error):
    return make_response('415 Unsupported Media Type', 415)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response('Internal Server Error', 500)


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'Message': 'Hello'})


@app.route('/')
def welcome():
    return """
      <h1> Welcome to GotIt Blog Service</h1>
      Api Docs
      <ul>
         <li><a href="/apidocs/index.html?url=/api/v1.0/spec">Api Version 1.0</a></li>
      </ul>
    """


import users
import blogs
