import jwt, datetime, time
from flask import jsonify, request, flash
from app.users.model import Users
from .. import config
from .. import common
from functools import wraps

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        Generate JWT Token
        """
        try:
            payload = {
                # expire time: 3600 seconds
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'iss': 'roger',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Verify JWT Token
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=600))
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': True})
            
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token expired! Please login again!'
        except jwt.InvalidTokenError:
            return 'Invalid Token.'


    def authenticate(self, email, password):
        """
        User Login & Authentication
        """
        userInfo = Users.query.filter_by(email=email).first()
        if (userInfo is None):
            return jsonify(common.returnFalseMsg('', 'Cannot find the user.'))
        else:
            if (Users.check_password(Users, userInfo.password, userInfo.salt, password)):
                login_time = int(time.time())
                userInfo.login_time = login_time
                Users.update(Users)
                token = self.encode_auth_token(userInfo.id, login_time)
                return jsonify(common.returnTrueMsg(token.decode(), 'Login success.'))
            else:
                return jsonify(common.returnFalseMsg('', 'Wrong password.'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        auth_header = request.headers.get('Authorization')
        
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = common.returnFalseMsg('', 'Please check HTTP Header format.')
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                
                if not isinstance(payload, str):    
                    user = Users.get(Users, payload['data']['id'])
                    if (user is None):
                        result = common.returnFalseMsg('', 'Cannot find the user.')
                    else:
                        if (user.login_time == payload['data']['login_time']):
                            return f(user.id, *args, **kwargs)
                        else:
                            result = common.returnFalseMsg('', 'Token has changed, please login again.')
                else:
                    result = common.returnFalseMsg('', payload)
        else:
            result = common.returnFalseMsg('', 'Please provide the auth-token.')
        
        return jsonify(result), 401

    return decorated_function
