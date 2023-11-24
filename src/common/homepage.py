from bottle import (
    get,
    post, 
    request, 
    HTTPResponse, 
    response, 
    redirect, 
    HTTPError, 
    static_file,
    Bottle,
    template
)
from urls import *

home = Bottle()

@home.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='/app/src/static')

@home.get(GHOMEPAGE)
def root():
    return template('index')
