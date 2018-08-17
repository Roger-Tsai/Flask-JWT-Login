DB_USER = 'DB_USER'
DB_PASSWORD = 'DB_PASSWORD'
DB_HOST = 'DB_HOST(IP or HostName)'
DB_DB = 'DB_NAME'

DEBUG = True
PORT = 8888
HOST = "127.0.0.1"
SECRET_KEY = "this is my secret key."

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB + '?charset=utf8'