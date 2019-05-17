import os

# General config
URL_PREFIX = os.getenv('URL_PREFIX', '/api/v1.0')
LOGGING_FILE_CONFIG = os.getenv('LOGGING_FILE_CONFIG', 'logging.conf')
LOG_FILE = os.getenv('LOG_FILE', 'd:\\gotit-blog-api.log')
# MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST', '10.1.36.167')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_DB = os.getenv('MYSQL_DB', 'gotit_blog')
MYSQL_USER = os.getenv('MYSQL_USER', 'gotit_blog')
MYSQL_PASS = os.getenv('MYSQL_PASS', 'gotit@2019')
MYSQL_POOL_SIZE = int(os.getenv('MYSQL_POOL_SIZE', '20'))
# Config Swagger
SWAGGER_CONFIG = {
    'description': 'GotIt Blog Service Specs',
    'termsOfService': 'Terms Of Service',
    'specs': [
        {
            'version': '1.0',
            'title': 'GotIt Blog Service v1.0',
            'endpoint': 'api_v1_spec',
            'route': '/api/v1.0/spec',
            'description': 'GotIt Blog Service Description',
            "rule_filter": lambda rule: rule.endpoint.startswith('v1')
        }
    ],
    'title': 'GotIt Blog Service Specs'
}
