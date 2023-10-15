from bottle import run as r
from bottle import route as rt
from bottle import (
    get,
    post, 
    request, 
    HTTPResponse, 
    response, 
    redirect, 
    HTTPError, 
    json_dumps
)

from user_db_manager import UserDBManager

@get('/register')
def register():
    return '''
        <form action="/register" method="post">
            User-String: <input name="request_string" type="text" />
            <input value="Register" type="submit" />
        </form>
    '''
    
@post('/register')
def do_register():
    base_model = UserDBManager()
    u_string = request.forms.get('request_string')
    req = {'request_string': u_string}
    print(req, 'bkendreq')
    if req.get('request_string') is not None:
        try:
            serializer = base_model.store_user_string(req).get('id')
            print(serializer, 'id')
            if serializer:
                get_secure_strings = base_model.deserialize_data(
                    serializer, 
                    'secured_user_string'
                )
                return HTTPResponse(
                    body=json_dumps(
                        {
                            'message': 'Success',
                            'secured_strings': get_secure_strings 
                        }
                    ),
                    status=201,
                    headers={
                        'Content-Type': 'text/plain',
                        'Set-Cookie': f'_id={serializer};\
                        Path=/'
                    }
                )
            else:
                return HTTPError(status=400)
        except Exception as e:
            print(f'Error during registration: {str(e)}')
            return HTTPResponse(
                body=json_dumps(
                    {'error': 'Internal Server Error. Please try again later.'}
                ),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    return HTTPError(status=401, body='Bad request')
        
        
@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            User_string: <input name="request_string" type="text" />
            <input value="Login" type="submit" />
        </form>
        <a href="/forgot-password"><button>Forgot Password</button></a>
    '''

@post('/login')
def do_login():
    get_id_from_cookie = request.get_cookie('_id')
    get_req_string = request.forms.get('request_string')
    model = UserDBManager(get_id_from_cookie)
    
    print(get_id_from_cookie, 'idddcook')
    req = {'uid': get_id_from_cookie, 'request_string' : get_req_string}
    print(req, 'reqqq')
    if req.get('uid') is not None and get_req_string is not None:
       try:
            verify = model.verify_user(req)
            print(verify, 'verify')
            if verify == 'Success':
               get_sus = model.deserialize_data(
                   get_id_from_cookie, 'secured_user_string'
                )
               return HTTPResponse(
                   body='Authentication Successful',
                   status=201,
                   headers={
                        'Content-Type': 'text/plain',
                        'Set-Cookie': f'sus={get_sus};\
                        Path=/login'
                    }
                )
            return HTTPError(status=403, body='Authentication failed, check login details')
       except Exception as e:
           print(e, '---> Error')
           return HTTPError(status=500, body='Server responded with failure, check back later')
    return HTTPError(status=403, body='User not found')


@get("/forgot-password")
def forgot_password():
    return '''
        <form action="/forgot-password" method="post">
            UserID: <input name="user_id" type="text" />
            Secure User String: <input name="sus" type="text" />
            <input value="Submit" type="submit" />
        </form>
        <a href="/login"><button>Abort</button></a>
    '''

r(host='localhost', port=8080, debug=True, reloader=True)