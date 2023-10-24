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
from urls import *

home = Bottle()


@home.get(GHOMEPAGE)
def root():
    return '''
            <p>Stashlet</p>
            <a href="/auth/register"><button>Get Started</button></a>

    '''