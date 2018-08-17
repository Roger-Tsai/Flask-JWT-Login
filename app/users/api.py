from flask import jsonify, request, Blueprint
from app.users.model import Users
from app.crawler.model import Pictures
from app.auth.auths import Auth, login_required
from .. import common

# User blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """
    User register
    """
    reqParams = request.get_json()
    email = reqParams['email'] if 'email' in reqParams else None
    username = reqParams['username'] if 'username' in reqParams else None
    password = reqParams['password'] if 'password' in reqParams else None
    
    # check if email exists
    user = Users.check_email_exists(Users, email)
    
    if not user:
        user = Users(email=email, username=username, password=password)
    else:
        return jsonify(common.returnFalseMsg('', 'Email exists'))
    
    result = Users.add(Users, user)
    
    if user.id:
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'login_time': user.login_time
        }
        return jsonify(common.returnTrueMsg(returnUser, "Register success."))
    else:
        return jsonify(common.returnFalseMsg('', 'Register fail.'))


@user_bp.route('/login', methods=['POST'])
def login():
    """
    User Login
    """
    reqParams = request.get_json()
    email = reqParams['email'] if 'email' in reqParams else None
    password = reqParams['password'] if 'password' in reqParams else None

    if (not email or not password):
        return jsonify(common.returnFalseMsg('', 'Username and password cannot be empty.'))
    else:
        return Auth.authenticate(Auth, email, password)

@user_bp.route('/info', methods=['GET'])
@login_required
def get_info(uid):
    """
    Get User Info
    """
    user = Users.get(Users, uid)
    returnUser = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'login_time': user.login_time
    }
    result = common.returnTrueMsg(returnUser, "Request success.")
    return jsonify(result)

# @user_bp.route('/pictures/<int:posterID>', methods=['GET'])
# @login_required
# def get_user_picture(posterID):

@user_bp.route('/ttt/<int:nnn>', methods=['GET'])
@login_required
def ttt(uid, nnn):

    print(request)
    print('QQQ:', uid, nnn)
    return jsonify({})
