from bottle import Bottle, get, static_file
from common.auth import auth
from common.homepage import home
from public.dashboard import dashboard


root = Bottle()




if __name__ == "__main__":
    root.merge(home)
    root.mount('/auth', auth)
    root.mount('/app', dashboard)
    root.run(host='localhost', port=8080, debug=True, reloader=True)

