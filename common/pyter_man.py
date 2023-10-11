from bottle import run as r
from bottle import route as rt
from bottle import get, post, request, HTTPResponse, response, redirect


from src.user_db_manager import UserDBManager

@get('/register') # or @route('/login')
def register():
    print(request.get_cookie, 'cookie-get')
    return '''
        <form action="/register" method="post">
            User-String: <input name="user_string" type="text" />
            <input value="Register" type="submit" />
        </form>
    '''
@post('/register')
def do_register():
    base_model = UserDBManager()

    # Get user_string from the form
    u_string = request.forms.get('user_string')
    print('User string:', u_string)

    # Update request dictionary
    req = {'request_string': u_string}

    # Store user string and get the user ID
    stored_user_data = base_model.store_user_string(req)
    get_uid = stored_user_data.get('id')
    print('User ID:', get_uid)

    # Deserialize secured_user_string
    des_sus = base_model.deserialize_data(get_uid, 'secured_user_string')
    print('Deserialized SUS:', des_sus)

    if des_sus is not None:
        # Set cookies
        response.set_header('Set-Cookie', 'kime=rime')
        response.set_cookie('sust', des_sus, secret='sus')

        return HTTPResponse(
            body="<p>Hello user, Registration successful </p>",
            status=200
        )
    else:
        return HTTPResponse(
            body="<p>Registration failed</p>",
            status=400
        )
        
r(host='localhost', port=8080, debug=True, reloader=True)