import shortuuid, uuid
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
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
from pydantic import ValidationError
from models import User
from redis_om import NotFoundError


@get('/register')
def register():
    return '''
        <form action="/register" method="post">
            User-String: <input name="request_string" type="text" />
            <input value="Register" type="submit" />
        </form>
        <a href="/login"><button>Already have an account</button></a>
    '''
    
@post('/register')
def do_register():
    u_string = request.forms.get('request_string')
    req = {'request_string': u_string}
    print(req, 'bkendreq')
    if req.get('request_string'):
        try:
            base_model = UserDBManager()
            serializer = base_model.store_user_string(req).get('id')
            print(serializer, 'id')
            if serializer:
                get_secure_strings = base_model.deserialize_data(
                    serializer, 
                    'secured_user_string'
                )
                expiration_date = datetime.now() + timedelta(days=2)
                expires = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
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
                        'Set-Cookie': f'uid={serializer}; Expires={expires}; Path=/'
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
    print(request.cookies.get('profile_id'))
    return '''
        <form action="/login" method="post">
            User_string: <input name="request_string" type="text" />
            <input value="Login" type="submit" />
        </form>
        <a href="/register"><button>Create Account</button></a>
        <a href="/forgot-password"><button>Forgot Password</button></a>
    '''

@post('/login')
def do_login():
    
    user_profile = request.cookies.get('profile_id')
    session_id = request.cookies.get('session_id')
    get_uid = request.cookies.get('uid')
    print(get_uid, 'guu')
    
    
    if not get_uid:
        return HTTPError(status=403, body='You do not have an account, please register')
    
    
    get_profile = user_profile
    if get_profile:

        try:
            get_user = User.get(user_profile)
            print(get_user, 'user')
            if get_user.session_id == session_id and get_user.is_authenticated:
                return redirect('/dashboard')
        except NotFoundError:
            print('User not found')
            pass
    print('empty profile')
    get_req_string = request.forms.get('request_string')
    req = {'uid': get_uid, 'request_string' : get_req_string}
    
    if get_uid and get_req_string:
       try:
            model = UserDBManager(get_uid)
            verify = model.verify_user(req)
            print(verify, 'verify')
            if verify == 'Success':
               get_sus = model.deserialize_data(
                   get_uid, 'secured_user_string'
                )
               
               print(get_sus, 'sus')
               expiration_date = datetime.now() + timedelta(days=2)
               expires = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
               print('Saving to REDIS')
               generate_unique_id = uuid.uuid4()
               encode_id_to_session = shortuuid.encode(generate_unique_id)
               try:
                user_profile = User(
                    ir_id = get_uid,
                    session_id = encode_id_to_session,
                    is_authenticated = True,
                )
               except ValidationError as e:
                   print('Error Found: ', e)
                   return
               user_profile.save()
               user_profile_id = user_profile.pk
               print('Saved to REDIS')
               profile = {
                    "session_id": encode_id_to_session,
                    "profile_id" : user_profile_id,
               }
               session_cookie = f'session_id={profile["session_id"]}; Path=/; Expires={expires};'
               profile_cookie = f'profile_id={profile["profile_id"]}; Path=/; Expires={expires};'
               
               responsed = HTTPResponse(body='Authentication Successful', status=201)
               responsed.add_header('Set-Cookie', profile_cookie)
               responsed.add_header('Set-Cookie', session_cookie)
               
               return responsed

            return HTTPError(status=403, body='Authentication failed, check login details')
       except Exception as e:
           print(e)
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
    

@post('/forgot-password')
def do_forgot_password():
    get_uid = request.forms.get('user_id')
    get_sus = request.forms.get('sus')
    model = UserDBManager(get_uid)
    if not get_sus and not get_uid:
        return HTTPError(status=400)
    req = {}
    req.update(uid= get_uid, secured_user_string = get_sus)
    x = model.check_sus_integrity(req)
    if x == 'Success':
        HTTPResponse(body='Validation completed, redirecting..', status=200)
        return redirect("/enter-new-string", code=302)
    HTTPError(status=403)    
    return redirect('/login')


@get('/enter-new-string')
def enter_new_strings():
    return '''
        <form action="/enter-new-string" method="post">
            User_String: <input name="user_string" type="text" />
            <input value="Submit" type="submit" />
        </form>
        <a href="/login"><button>Return to Login Page⬅️</button></a>
    '''


@post('/enter-new-string')
def do_enter_new_string():
    new_user_string = request.forms.get('user_string')
    get_id = request.cookies.get('_id')
    if not new_user_string and not get_id:
        return HTTPError(status=400)
    request_data = {'_id': get_id, 'user_string' : new_user_string}
    print(request_data, 'enter')
    model = UserDBManager(get_id)
    response_data = model.recover_account(request_data)
    print(response_data, 'rdd')
    if response_data:
        # get_uid = response_data.get('_id')
        get_new_sus = response_data.get('sus')
        return HTTPResponse(
            body='Account Recovered Successfully, check mail for details..',
            status=200,
            headers={
                    'Content-Type': 'text/plain',
                    'Set-Cookie': f'new_sus={get_new_sus};\
                    Path=/login'
                }
        )
    return HTTPError(status=400)


@get('/dashboard')
def dashboard():
    return '''
            <p>Welcome Home</p>
            <a href="/logout"><button>Logout⬅️</button></a>
    '''
        


@get('/logout')
def do_logout():
    get_profile = request.cookies.get('profile_id')
    if not get_profile:
        return redirect('/login')

    # Delete cookies from the response to log the user out
    response.delete_cookie('profile_id')
    response.delete_cookie('session_id')
    
    try:
        user = User.get(get_profile)
        user.session_id = None
        user.is_authenticated = False
        user.save()
    except Exception as e:
        print(f"Error while logging out: {e}")
        
    return redirect('/login')

    
    
    
     
r(host='localhost', port=8080, debug=True, reloader=True)