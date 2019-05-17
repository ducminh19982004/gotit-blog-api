import logging.config

from flask import Flask
from flasgger import Swagger

import mysql.connector
from mysql.connector import pooling

from config import (
    LOG_FILE,
    LOGGING_FILE_CONFIG,
    SWAGGER_CONFIG,
    MYSQL_DB,
    MYSQL_HOST,
    MYSQL_PASS,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_POOL_SIZE,
)

app = Flask(__name__)
app.config['SWAGGER'] = SWAGGER_CONFIG
Swagger(app)

logging.config.fileConfig(LOGGING_FILE_CONFIG, defaults={'logfilename': LOG_FILE})
logger = logging.getLogger('sLogger')

db = mysql.connector.pooling.MySQLConnectionPool(pool_name="mysql_pool",
                                                 pool_size=MYSQL_POOL_SIZE,
                                                 pool_reset_session=True,
                                                 host=MYSQL_HOST,
                                                 port=MYSQL_PORT,
                                                 database=MYSQL_DB,
                                                 user=MYSQL_USER,
                                                 password=MYSQL_PASS)

import service
