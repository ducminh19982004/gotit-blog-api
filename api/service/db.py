from api import (
    db,
    logger,
)
from api.utilities import (
    log_exception,
)


def close_db_connection(conn):
    """
    :param conn:
    :return:
    """
    if conn and conn.is_connected():
        conn.close()


def close_cursor_connection(cursor):
    """
    :param cursor:
    :return:
    """
    if cursor:
        cursor.close()


def login(email, sso_id, login_type):
    """
    :param email:
    :param sso_id:
    :param login_type:
    :return:
        code: '-1: error, 0: success, 1: need more info for login via Google,
                2: need more info for login via Facebook, 3: wrong logic'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            sql = "Select full_name, mobile_number, occupation, facebook_id, google_id from users " \
                  "where email = '%s' order by id desc limit 0,1" \
                  % email
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                """User existed"""
                for row in rows:
                    full_name = row['full_name']
                    mobile_number = row['mobile_number']
                    occupation = row['occupation']
                    facebook_id = row['facebook_id']
                    google_id = row['google_id']
                    if login_type == 1:
                        """Login via Google"""
                        if google_id is not None and sso_id == google_id:
                            if full_name is not None and occupation is not None:
                                """Full Name and Occupation are enough"""
                                code = 0
                            else:
                                code = 1
                        else:
                            code = 3
                    if login_type == 2:
                        """Login via Facebook"""
                        if facebook_id is not None and sso_id == facebook_id:
                            if full_name is not None and mobile_number is not None:
                                """Full Name and Mobile Number are enough"""
                                code = 0
                            else:
                                code = 2
                        else:
                            code = 3
            else:
                """User is not existed"""
                """Login via Google"""
                code = 1
                sql = "Insert into users (email,google_id,login_time) values ('%s','%s', now())" % (email, sso_id)
                if login_type == 2:
                    """Login via Facebook"""
                    code = 2
                    sql = "Insert into users (email,facebook_id,login_time) values ('%s','%s', now())" % (email, sso_id)
                logger.info(sql)
                cursor.execute(sql)
                conn.commit()

    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def update_user_info(email, login_type, full_name, mobile_number, occupation):
    """
    :param email:
    :param login_type:
    :param full_name:
    :param mobile_number:
    :param occupation:
    :return:
        code: '-1: error, 0: success, 1: user is not existed, 2: wrong logic'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            sql = "Select google_id, facebook_id from users " \
                  "where email = '%s' order by id desc limit 0,1" \
                  % email
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    google_id = row['google_id']
                    facebook_id = row['facebook_id']
                    if login_type == 1:
                        """Login via Google"""
                        if google_id is None:
                            code = 2
                        else:
                            sql = "Update users set full_name = '%s', occupation = '%s', status = 1 " \
                                  "where email = '%s'" % (full_name, occupation, email)
                            logger.info(sql)
                            cursor.execute(sql)
                            conn.commit()
                            code = 0
                    if login_type == 2:
                        """Login via Facebook"""
                        if facebook_id is None:
                            code = 2
                        else:
                            sql = "Update users set full_name = '%s', mobile_number = '%s', status = 1 " \
                                  "where email = '%s'" % (full_name, mobile_number, email)
                            logger.info(sql)
                            cursor.execute(sql)
                            conn.commit()
                            code = 0
            else:
                """User is not existed"""
                code = 1
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def get_user_info(email):
    """
    :param email:
    :return:
        code: '-1: error, 0: success, 1: user is not existed'
        info: {
            'email':email,
            'full_name': full_name,
            'mobile_number': mobile_number,
            'occupation': mobile_number,
        }
    """
    conn = None
    cursor = None
    code = -1
    info = {}
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            sql = "Select id, email, full_name, mobile_number,occupation from users " \
                  "where email = '%s' order by id desc limit 0,1" \
                  % email
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    info['id'] = row['id']
                    info['email'] = row['email']
                    info['full_name'] = row['full_name']
                    info['mobile_number'] = row['mobile_number']
                    info['occupation'] = row['occupation']
                code = 0
            else:
                """User is not existed"""
                code = 1
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code, info


def check_user_active(user_id):
    """
    :param user_id:
    :return:
        code: '-1: error, 0: success, 1: user is not existed, 2: user not active'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            sql = "Select id, status from users " \
                  "where id = '%s' order by id desc limit 0,1" \
                  % user_id
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    if row['status'] == 0:
                        code = 2
                    if row['status'] == 1:
                        code = 0
            else:
                """User is not existed"""
                code = 1
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def create_blog(user_id, title, content):
    """
    :param user_id:
    :param title:
    :param content:
    :return:
        code: '-1: error, 0: success'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            sql = "Insert into blogs (user_id,title,content) values (%s,'%s','%s')" % (user_id, title, content)
            logger.info(sql)
            cursor.execute(sql)
            conn.commit()
            code = 0
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def like_blog(blog_id, user_id):
    """
    :param blog_id:
    :param user_id:
    :return:
        code: '-1: error, 0: success, 3: blog is not existed'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            sql = "Select id from blogs where id = %s" % blog_id
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                sql = "Insert into like_blog (blog_id, user_id) values (%s,%s) " \
                      "on duplicate key update created_time = now()" \
                      % (blog_id, user_id)
                logger.info(sql)
                cursor.execute(sql)
                conn.commit()
                code = 0
            else:
                code = 3
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def update_blog(blog_id, user_id, title, content):
    """
    :param blog_id:
    :param user_id:
    :param title:
    :param content:
    :return:
        code: '-1: error, 0: success, 3: blog is not existed'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            sql = "Select id from blogs where id = %s and user_id = %s " % (blog_id, user_id)
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                sql = "Update blogs set title = '%s', content = '%s', udpated_time = now() " \
                      "where id = %s and user_id = %s" % (title, content, blog_id, user_id)
                logger.info(sql)
                cursor.execute(sql)
                conn.commit()
                code = 0
            else:
                code = 3
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def delete_blog(blog_id, user_id):
    """
    :param blog_id:
    :param user_id:
    :return:
        code: '-1: error, 0: success, 3: blog is not existed'
    """
    conn = None
    cursor = None
    code = -1
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            sql = "Select id from blogs where id = %s and user_id = %s " % (blog_id, user_id)
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                sql = "Delete from blogs where id = %s and user_id = %s" % (blog_id, user_id)
                logger.info(sql)
                cursor.execute(sql)
                conn.commit()
                code = 0
            else:
                code = 3
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code


def get_blog_detail(blog_id):
    """
    :param blog_id:
    :return:
        code: '-1: error, 0: success, 3: blog is not existed'
        info = {
            'id': id,
            'title' : title,
            'content': content,
        }
    """
    conn = None
    cursor = None
    code = -1
    info = {}
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            sql = "Select id, title, content from blogs where id = %s" % blog_id
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    info['id'] = row['id']
                    info['title'] = row['title']
                    info['content'] = row['content']
                code = 0
            else:
                code = 3
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code, info


def list_blogs_by_user(user_id, page, size):
    """
    :param user_id:
    :param page:
    :param size:
    :return:
        code: '-1: error, 0: success'
        info = [
            {
                'id': id,
                'title' : title,
                'content': content,
            }
        ]
    """
    conn = None
    cursor = None
    code = -1
    list_blogs = []
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            offset = (page - 1) * size
            sql = "Select id, title, content from blogs " \
                  "where user_id = %s order by updated_time, created_time desc limit %s,%s" % (user_id, offset, size)
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    info = {
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                    }
                    list_blogs.append(info)
            code = 0
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code, list_blogs


def list_blogs(page, size):
    """
    :param page:
    :param size:
    :return:
        code: '-1: error, 0: success'
        info = [
            {
                'id': id,
                'title' : title,
                'content': content,
            }
        ]
    """
    conn = None
    cursor = None
    code = -1
    list_blogs = []
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            offset = (page - 1) * size
            sql = "Select id, title, content from blogs " \
                  "order by updated_time, created_time desc limit %s,%s" % (offset, size)
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    info = {
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                    }
                    list_blogs.append(info)
            code = 0
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code, list_blogs


def list_user_like_blog(blog_id):
    """
    :param blog_id:
    :return:
        code: '-1: error, 0: success'
        info = [
            {
                'id': id,
                'full_name' : title,
            }
        ]
    """
    conn = None
    cursor = None
    code = -1
    list_users = []
    try:
        conn = db.get_connection()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            sql = "Select a.id, a.full_name from users a, like_blog b where a.id = b.user_id and b.blog_id = %s " \
                  "order by b.created_time desc" % blog_id
            logger.info(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    info = {
                        'id': row['id'],
                        'full_name': row['full_name'],
                    }
                    list_users.append(info)
            code = 0
    except Exception as e:
        log_exception(e)
    finally:
        close_cursor_connection(cursor)
        close_db_connection(conn)
    return code, list_users
