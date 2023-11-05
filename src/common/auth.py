import shortuuid, uuid, time
from http.cookies import SimpleCookie
from datetime import datetime, timedelta
from bottle import Bottle
from bottle import (
    get,
    route,
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
from models import User, Session
from redis_om import NotFoundError
from .common_urls import *
from urls import *
from status import *

auth = Bottle()



@auth.route(REGISTER)
def register():
    return '''
        <form action="/auth/register" method="post">
            User-String: <input name="request_string" type="text" />
            <input value="Register" type="submit" />
        </form>
        <a href="/auth/login"><button>Already have an account</button></a>
    '''
    
    
@auth.route(REGISTER, method='POST')
def do_register():
    u_string = request.forms.get('request_string')
    req = {'request_string': u_string}
    print(req, 'bkendreq')
    
    if req.get('request_string'):
        try:
            base_model = UserDBManager()#TODO maybe use sus to login instaed of ustring
            serializer = base_model.store_user_string(req).get('id')
            print(serializer, 'id')
            
            if serializer:
                get_secure_strings = base_model.deserialize_data( #check init
                    serializer, 
                    'secured_user_string'
                )
                
                print(get_secure_strings)
                
                expiration_date = datetime.now() + timedelta(days=2)
                cookie_expires = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
                
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
                        'Set-Cookie': f'uid={serializer}; Expires={cookie_expires}; Path={GHOMEPAGE}'
                    }
                )
            return HTTPError(status= HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f'Error during registration: {str(e)}')
            return HTTPError(status= HTTP_500_INTERNAL_SERVER_ERROR)
            
    return HTTPError(status= HTTP_400_BAD_REQUEST, body='Empty request body')
        
        
@auth.route(LOGIN)
def login():
    user_profile = request.cookies.get('profile_id')
    
    session_id = request.cookies.get('session_id')
    
    get_uid = request.cookies.get('uid')
    
    get_profile = user_profile
    if get_profile:

        try:
            get_user = Session.get(user_profile)
            if get_user.session_id == session_id and get_user.is_authenticated:
                return redirect(GHOME, code= HTTP_303_SEE_OTHER)
        except NotFoundError:
            print('User not found')
            pass
        
    return '''
        <form action="/auth/login" method="post">
            User_string: <input name="request_string" type="text" />
            <input value="Login" type="submit" />
        </form>
        <a href="/auth/register"><button>Create Account</button></a>
        <a href="/auth/forgot-password"><button>Forgot Password</button></a>
    '''


@auth.route(LOGIN, method='POST')
def do_login():
    u_string = request.forms.get('request_string')
    
    if not u_string:
        return HTTPError(status=HTTP_400_BAD_REQUEST)
    
    get_uid = request.cookies.get('uid')
    
    if not get_uid:
        return HTTPError(status=HTTP_401_UNAUTHORIZED, body='You do not have an account, please register')

    get_req_string = request.forms.get('request_string')
    req = {'uid': get_uid, 'request_string' : u_string}
    
    if get_uid and get_req_string:
       try:
            model = UserDBManager(get_uid)
            verify = model.verify_user(req)
            print(verify, 'verify')
            
            if verify == 'Success':
               get_sus = model.deserialize_data(
                   get_uid, 'secured_user_string'
                )
               
               expiration_date = datetime.now() + timedelta(days=2)
               cookie_expires = expiration_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
               generate_unique_id = uuid.uuid4()
               encode_id_to_session = shortuuid.encode(generate_unique_id)
               
               try:
                user_session = Session(
                    session_id = encode_id_to_session,
                    is_authenticated = True,
                )
               except ValidationError as e:
                   print(e)
                   return
               
               user_session.save()
               
               expiration_time = time.time() + (2 * 24 * 60 * 60) 
               user_session.expire(int(expiration_time - time.time()))
               
               user_session_id = user_session.pk
               
               profile = {
                    "session_id": encode_id_to_session,
                    "profile_id" : user_session_id, #query redis collection
               }
               
               session_cookie = f'session_id={profile["session_id"]}; Path={GHOMEPAGE}; Expires={cookie_expires};'
               profile_cookie = f'profile_id={profile["profile_id"]}; Path={GHOMEPAGE}; Expires={cookie_expires};'
               
               responsed = HTTPResponse(body='Authentication Successful', status=201)
               responsed.add_header('Set-Cookie', profile_cookie)
               responsed.add_header('Set-Cookie', session_cookie)
               
               return responsed

            return HTTPError(status=HTTP_401_UNAUTHORIZED, body='Authentication failed, check login details')
       except Exception as e:
           print(e)
           return HTTPError(status=HTTP_500_INTERNAL_SERVER_ERROR, body='Server responded with failure, check back later')
       
    return HTTPError(status= HTTP_400_BAD_REQUEST)


@auth.route(FORGOT_PASSWORD)
def forgot_password():
    
    return '''
        <form action="/auth/forgot-password" method="post">
            UserID: <input name="user_id" type="text" />
            Secure User String: <input name="sus" type="text" />
            <input value="Submit" type="submit" />
        </form>
        <a href="/auth/login"><button>Abort</button></a>
    '''
    

@auth.route(FORGOT_PASSWORD, method='POST')
def do_forgot_password():
    get_uid = request.forms.get('user_id')
    
    get_sus = request.forms.get('sus')
    
    if not get_sus or not get_uid:
        return HTTPError(status= HTTP_400_BAD_REQUEST)
    
    model = UserDBManager(get_uid)
    
    req = {}
    
    req.update(uid= get_uid, secured_user_string = get_sus)
    
    x = model.check_sus_integrity(req)
    
    if x == 'Success':
        HTTPResponse(body='Validation completed, redirecting..', status=200)
        return redirect(GENTER_NEW_STRING, code= HTTP_303_SEE_OTHER)
    
    error = HTTPError(status= HTTP_401_UNAUTHORIZED)    
    
    return error, redirect(GLOGIN, code= HTTP_303_SEE_OTHER)



@auth.route(ENTER_NEW_STRING)
def enter_new_strings():
    
    return '''
        <form action="/auth/enter-new-string" method="post">
            User_String: <input name="user_string" type="text" />
            <input value="Submit" type="submit" />
        </form>
        <a href="/auth/login"><button>Return to Login Page⬅️</button></a>
    '''


@auth.route(ENTER_NEW_STRING, method='POST')
def do_enter_new_string():
    new_user_string = request.forms.get('user_string')
    
    get_id = request.cookies.get('_id')
    
    if not new_user_string or not get_id:
        return HTTPError(status=HTTP_400_BAD_REQUEST)
    
    request_data = {'_id': get_id, 'user_string' : new_user_string}
    
    print(request_data, 'enter')
    
    model = UserDBManager(get_id)
    
    response_data = model.recover_account(request_data)
    
    print(response_data, 'rdd')
    
    if response_data:
        # get_uid = response_data.get('_id')
        get_new_sus = response_data.get('sus')
        
        return HTTPResponse(
            body='Account Recovered Successfully, check mail for details..',#TODO Respond with email
            status= HTTP_201_CREATED,
            headers={
                    'Content-Type': 'text/plain',
                    'Set-Cookie': f'new_sus={get_new_sus};\
                    Path={GHOME}'
                }
        )
        
    return HTTPError(status=400)


@auth.route(LOGOUT)
def do_logout():
    get_profile = request.cookies.get('profile_id')
    
    if not get_profile:
        return redirect(GHOMEPAGE)
    
    Session.delete(get_profile)

    # Delete cookies from the response to log the user out
    response.delete_cookie('profile_id', path=GHOMEPAGE)
    response.delete_cookie('session_id', path=GHOMEPAGE)
    
    return redirect(GHOMEPAGE, code= HTTP_302_FOUND)


@auth.route(CLOSE_ACCOUNT)
def close_account():

    user_profile = request.cookies.get('profile_id')
    
    session_id = request.cookies.get('session_id')
    
    if user_profile and session_id:

        try:
            get_user = Session.get(user_profile)
            if get_user.session_id == session_id and get_user.is_authenticated:
                return '''
                    <form action="/auth/close-account" method="post">
                        Secure User String: <input name="sus" type="text" />
                        <input value="Submit" type="submit" />
                    </form>
                    <a href="/auth/login"><button>Cancel⬅️</button></a>
                '''
        except NotFoundError:
            return HTTPError(status=HTTP_403_FORBIDDEN, body='You do not have the required permissions to access this resource')
    return redirect(GLOGIN)


@auth.route(CLOSE_ACCOUNT, method='POST')
def do_close_account():
    user_id = request.cookies.get('uid')
    secure_user_string = request.forms.get('sus')
    user_profile = request.cookies.get('profile_id')
    
    
    if not user_id:
        return redirect(GREGISTER)
    if not secure_user_string:
        return HTTPError(status=HTTP_400_BAD_REQUEST, body='Validation Error')
    
    req = {'uid': user_id, 'sus': secure_user_string}
    try:
        data = UserDBManager(user_id).close_account(req)
        if data == 'Success':
            #delete user session in session model
            Session.delete(user_profile)
            
            # Delete cookies in the user-agent
            response.delete_cookie('profile_id', path=GHOMEPAGE)
            response.delete_cookie('session_id', path=GHOMEPAGE)
            response.delete_cookie('uid', path=GHOMEPAGE)

            return redirect(GHOMEPAGE)
        return HTTPError(body='Error closing account, kindly check details and try again')
    except KeyError as e:
        return HTTPError(status=HTTP_400_BAD_REQUEST)

