from cerberus import Validator


def validate_api_login(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'email': {'required': True, 'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'sso_id': {'required': True, 'type': 'string'},
        'login_type': {'required': True, 'type': 'integer', 'allowed': [1, 2]},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_get_user_info(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'email': {'required': True, 'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_update_user_info(data_input, login_type):
    """
    :param data_input:
    :param login_type:
    :return:
    """
    schema = {
        'email': {'required': True, 'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'login_type': {'required': True, 'type': 'integer', 'allowed': [1, 2]},
        'full_name': {'required': True, 'type': 'string'},
        'mobile_number': {'type': 'number', 'nullable': True},
        'occupation': {'required': True, 'type': 'string'},
    }
    if login_type == 2:
        schema = {
            'email': {'required': True, 'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            'login_type': {'required': True, 'type': 'integer', 'allowed': [1, 2]},
            'full_name': {'required': True, 'type': 'string'},
            'mobile_number': {'required': True, 'type': 'number'},
            'occupation': {'nullable': True, 'type': 'string'},
        }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_create_blog(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'user_id': {'required': True, 'type': 'integer'},
        'title': {'required': True, 'type': 'string'},
        'content': {'required': True, 'type': 'string'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_like_blog(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'user_id': {'required': True, 'type': 'integer'},
        'blog_id': {'required': True, 'type': 'integer'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_get_blog(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'user_id': {'required': True, 'type': 'integer'},
        'blog_id': {'required': True, 'type': 'integer'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_delete_blog(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'user_id': {'required': True, 'type': 'integer'},
        'blog_id': {'required': True, 'type': 'integer'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_list_blog(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'user_id': {'required': True, 'type': 'integer'},
        'page': {'required': True, 'type': 'integer'},
        'size': {'required': True, 'type': 'integer'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors


def validate_api_list_user_like_blog(data_input):
    """
    :param data_input:
    :return:
    """
    schema = {
        'user_id': {'required': True, 'type': 'integer'},
        'blog_id': {'required': True, 'type': 'integer'},
    }
    v = Validator(schema)
    if v.validate(data_input):
        return True, data_input
    else:
        return False, v.errors
