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


@app.route(URL_PREFIX + '/createBlog', methods=['post'], endpoint='v1_create_blog')
@authen.authen_required
def create_blog():
    """
        Create blog
        ---
        tags:
          - Blog
        parameters:
          - in: body
            name: blog
            required: true
            description: Blog info
            schema:
              id: blog
              required:
                - user_id
                - title
                - content
              properties:
                user_id:
                  type: integer
                  required: true
                  description: User ID
                title:
                  type: string
                  required: true
                  description: Title
                content:
                  type: string
                  required: true
                  description: Content
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active'
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        if request.headers['Content-Type'] == 'application/json':
            body = request.json
            validate, error_detail = schema.validate_api_create_blog(body)
            if validate:
                code = db.check_user_active(body['user_id'])
                if code == 0:
                    code = db.create_blog(body['user_id'], body['title'], body['content'])
                return jsonify({'code': code}), 200
            else:
                return jsonify(error_detail), 400
        else:
            abort(415)
    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/likeBlog', methods=['get'], endpoint='v1_like_blog')
@authen.authen_required
def like_blog():
    """
        Like
        ---
        tags:
          - Blog
        parameters:
          - in: query
            name: blog_id
            type: integer
            required: true
            description: Blog ID
          - in: query
            name: user_id
            type: integer
            required: true
            description: User ID
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active'
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        user_id = request.args.get('user_id')
        if user_id is None:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            pass
        blog_id = request.args.get('blog_id')
        if blog_id is None:
            abort(400)
        try:
            blog_id = int(blog_id)
        except:
            pass
        info = {
            'blog_id': blog_id,
            'user_id': user_id,
        }
        validate, error_detail = schema.validate_api_like_blog(info)
        if validate:
            code = db.check_user_active(user_id)
            if code == 0:
                code = db.like_blog(blog_id, user_id)
            return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400

    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/getBlog', methods=['get'], endpoint='v1_get_blog_detail')
@authen.authen_required
def get_blog_detail():
    """
        Blog detail
        ---
        tags:
          - Blog
        parameters:
          - in: query
            name: blog_id
            type: integer
            required: true
            description: Blog ID
          - in: query
            name: user_id
            type: integer
            required: true
            description: User ID Login
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active'
                info:
                  type: object
                  required: true
                  properties:
                    id:
                      type: integer
                    title:
                      type: string
                    content:
                      type: string
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        user_id = request.args.get('user_id')
        if user_id is None:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            pass
        blog_id = request.args.get('blog_id')
        if blog_id is None:
            abort(400)
        try:
            blog_id = int(blog_id)
        except:
            pass
        info = {
            'blog_id': blog_id,
            'user_id': user_id,
        }
        validate, error_detail = schema.validate_api_get_blog(info)
        if validate:
            code = db.check_user_active(user_id)
            if code == 0:
                code, info = db.get_blog_detail(blog_id)
            return jsonify({'code': code, 'info': info}), 200
        else:
            return jsonify(error_detail), 400

    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/deleteBlog', methods=['delete'], endpoint='v1_delete_blog')
@authen.authen_required
def delete_blog():
    """
        Delete Blog
        ---
        tags:
          - Blog
        parameters:
          - in: query
            name: blog_id
            type: integer
            required: true
            description: Blog ID
          - in: query
            name: user_id
            type: integer
            required: true
            description: User ID Login
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active, 3: blog is not existed'
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        user_id = request.args.get('user_id')
        if user_id is None:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            pass
        blog_id = request.args.get('blog_id')
        if blog_id is None:
            abort(400)
        try:
            blog_id = int(blog_id)
        except:
            pass
        info = {
            'blog_id': blog_id,
            'user_id': user_id,
        }
        validate, error_detail = schema.validate_api_delete_blog(info)
        if validate:
            code = db.check_user_active(user_id)
            if code == 0:
                code = db.delete_blog(blog_id, user_id)
            return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400

    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/listBlog', methods=['get'], endpoint='v1_list_blog')
@authen.authen_required
def list_blog():
    """
        List Blog
        ---
        tags:
          - Blog
        parameters:
          - in: query
            name: user_id
            type: integer
            required: true
            description: User ID Login
          - in: query
            name: page
            type: integer
            required: true
            description: Page
          - in: query
            name: size
            type: integer
            required: true
            description: Size
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active'
                info:
                  type: array
                  required: true
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        user_id = request.args.get('user_id')
        if user_id is None:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            pass
        page = request.args.get('page')
        if page is None:
            abort(400)
        try:
            page = int(page)
        except:
            pass
        size = request.args.get('size')
        if size is None:
            abort(400)
        try:
            size = int(size)
        except:
            pass
        info = {
            'user_id': user_id,
            'page': page,
            'size': size,
        }
        validate, error_detail = schema.validate_api_list_blog(info)
        if validate:
            code = db.check_user_active(user_id)
            if code == 0:
                code, lists = db.list_blogs(page, size)
                return jsonify({'code': code, 'info': lists}), 200
            else:
                return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400
    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/listBlogByUser', methods=['get'], endpoint='v1_list_blog_by_user')
def list_blog_by_user():
    """
        List Blog by User
        ---
        tags:
          - Blog
        parameters:
          - in: query
            name: user_id
            type: integer
            required: true
            description: User ID Login
          - in: query
            name: page
            type: integer
            required: true
            description: Page
          - in: query
            name: size
            type: integer
            required: true
            description: Size
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active'
                info:
                  type: array
                  required: true
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        user_id = request.args.get('user_id')
        if user_id is None:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            pass
        page = request.args.get('page')
        if page is None:
            abort(400)
        try:
            page = int(page)
        except:
            pass
        size = request.args.get('size')
        if size is None:
            abort(400)
        try:
            size = int(size)
        except:
            pass
        info = {
            'user_id': user_id,
            'page': page,
            'size': size,
        }
        validate, error_detail = schema.validate_api_list_blog(info)
        if validate:
            code = db.check_user_active(user_id)
            if code == 0:
                code, lists = db.list_blogs_by_user(user_id, page, size)
                return jsonify({'code': code, 'info': lists}), 200
            else:
                return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400
    except Exception as e:
        log_exception(e)
        abort(500)


@app.route(URL_PREFIX + '/listUserLikeBlog', methods=['get'], endpoint='v1_list_user_like_blog')
def list_user_like_blog():
    """
        List User Like Blog
        ---
        tags:
          - Blog
        parameters:
          - in: query
            name: user_id
            type: integer
            required: true
            description: User ID Login
          - in: query
            name: blog_id
            type: integer
            required: true
            description: Blog ID
        responses:
          200:
            description: Ok
            schema:
              properties:
                code:
                  type: integer
                  required: true
                  description: '-1: error, 0: success, 1: user is not existed,
                                  2: user not active'
                info:
                  type: array
                  required: true
          400:
            description: Bad Request
          500:
            description: Internal Server Error
    """
    try:
        """Validate parameters"""
        user_id = request.args.get('user_id')
        if user_id is None:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            pass
        blog_id = request.args.get('blog_id')
        if blog_id is None:
            abort(400)
        try:
            blog_id = int(blog_id)
        except:
            pass
        info = {
            'user_id': user_id,
            'blog_id': blog_id,
        }
        validate, error_detail = schema.validate_api_list_user_like_blog(info)
        if validate:
            code = db.check_user_active(user_id)
            if code == 0:
                code, lists = db.list_user_like_blog(blog_id)
                return jsonify({'code': code, 'info': lists}), 200
            else:
                return jsonify({'code': code}), 200
        else:
            return jsonify(error_detail), 400
    except Exception as e:
        log_exception(e)
        abort(500)
