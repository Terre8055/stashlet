import shortuuid, uuid, time
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
from bottle import (
    get,
    post, 
    request, 
    HTTPResponse, 
    response, 
    redirect, 
    HTTPError, 
    json_dumps,
    Bottle
)


from user_db_manager import UserDBManager
from pydantic import ValidationError
from models import User, Session
from redis_om import NotFoundError
from .public_urls import *
from status import *
from urls import *

dashboard = Bottle()




@dashboard.route(HOME)
def root():#TODO verify sessions
    user_profile = request.cookies.get('profile_id')
    
    session_id = request.cookies.get('session_id')
    
    if user_profile and session_id:

        try:
            get_user = Session.get(user_profile)
            if get_user.session_id == session_id and get_user.is_authenticated:
                return '''
                        <p>Welcome Home</p>
                        <a href="/auth/logout"><button>Logout⬅️</button></a>
                        <a href="/auth/close-account"><button>Close Account</button></a>
                '''
        except NotFoundError:
            return HTTPError(status=HTTP_403_FORBIDDEN, body='You do not have the required permissions to access this resource')
    return redirect(GLOGIN)
