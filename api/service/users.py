from flask import (
    request,
    abort,
    jsonify,
)

from api import (
    app,
    authen,
    schema,
)
from api.utilities import (
    log_exception,
)
from config import (
    URL_PREFIX,
)
import db


@app.route(URL_PREFIX + '/login', methods=['get'], endpoint='v1_login')
@authen.authen_required
def login():
    """
        Login
        ---
        tags:
          - User
        parameters:
          - in: query
            name: email
            type: string
            required: true
            description: Email
          - in: query
            name: sso_id
            type: string
            required: true
            description: Google ID or Facebook ID
          - in: query
            name: login_type
            type: integer
            required: true
            description: '1: login via Google, 2: login via Facebook'
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: need more info for login via Google,
                                  2: need more info for login via Facebook, 3: wrong logic'
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        email = request.args.get('email')
        if email is None:
            abort(400)
        sso_id = request.args.get('sso_id')
        if sso_id is None:
            abort(400)
        login_type = request.args.get('login_type')
        if login_type is None:
            abort(400)
        try:
            login_type = int(login_type)
        except:
            pass
        info = {
            'email': email,
            'sso_id': sso_id,
            'login_type': login_type
        }
        validate, error_detail = schema.validate_api_login(info)
        if validate:
            code = db.login(email, sso_id, login_type)
            return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400
    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/updateUserInfo', methods=['get'], endpoint='v1_update_user_info')
@authen.authen_required
def update_user_info():
    """
        Update User Info
        ---
        tags:
          - User
        parameters:
          - in: query
            name: email
            type: string
            required: true
            description: Email
          - in: query
            name: login_type
            type: integer
            required: true
            description: '1: login via Google, 2: login via Facebook'
          - in: query
            name: full_name
            type: string
            required: true
            description: Full Name
          - in: query
            name: mobile_number
            type: string
            required: false
            description: Mobile Number
          - in: query
            name: occupation
            type: string
            required: false
            description: Occupation
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed, 2: wrong logic'
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        email = request.args.get('email')
        if email is None:
            abort(400)
        login_type = request.args.get('login_type')
        if login_type is None:
            abort(400)
        try:
            login_type = int(login_type)
        except:
            pass
        full_name = request.args.get('full_name')
        if full_name is None:
            abort(400)
        mobile_number = request.args.get('mobile_number')
        try:
            mobile_number = long(mobile_number)
        except:
            pass
        occupation = request.args.get('occupation')
        info = {
            'email': email,
            'login_type': login_type,
            'full_name': full_name,
            'mobile_number': mobile_number,
            'occupation': occupation,
        }
        validate, error_detail = schema.validate_api_update_user_info(info, login_type)
        if validate:
            code = db.update_user_info(email, login_type, full_name, mobile_number, occupation)
            return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400
    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/getUserInfo', methods=['get'], endpoint='v1_get_user_info')
@authen.authen_required
def get_user_info():
    """
        Get User Info
        ---
        tags:
          - User
        parameters:
          - in: query
            name: email
            type: string
            required: true
            description: Email
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed'
                info:
                  type: object
                  required: true
                  properties:
                    id:
                      type: integer
                    email:
                      type: string
                    full_name:
                      type: string
                    mobile_number:
                      type: string
                    occupation:
                      type: string
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        email = request.args.get('email')
        if email is None:
            abort(400)
        info = {
            'email': email,
        }
        validate, error_detail = schema.validate_api_get_user_info(info)
        if validate:
            code, info = db.get_user_info(email)
            return jsonify({'code': code, 'info': info}), 200
        else:
            return jsonify(error_detail), 400
    except Exception as e:
        log_exception(e)
        abort(500)
