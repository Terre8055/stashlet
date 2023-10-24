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


dashboard = Bottle()




@dashboard.route(HOME)
def root():#TODO verify sessions
    return '''
            <p>Welcome Home</p>
            <a href="/auth/logout"><button>Logout⬅️</button></a>
    '''