import shortuuid, uuid, time
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
from bottle import (
    get,
    static_file,
    template, 
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


@dashboard.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='/app/src/static')


@dashboard.route(HOME)
def root():#TODO verify sessions
    user_profile = request.cookies.get('profile_id')
    
    session_id = request.cookies.get('session_id')
    
    if user_profile and session_id:

        try:
            get_user = Session.get(user_profile)
            if get_user.session_id == session_id and get_user.is_authenticated:
                return template('dashboard')
        except NotFoundError:
            return HTTPError(status=HTTP_403_FORBIDDEN, body='You do not have the required permissions to access this resource')
    return redirect(GLOGIN)
