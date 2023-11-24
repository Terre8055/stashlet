from bottle import Bottle, get, static_file, TEMPLATE_PATH
from common.auth import auth
from common.homepage import home
from public.dashboard import dashboard

TEMPLATE_PATH.append('/app/src/views')
root = Bottle()




if __name__ == "__main__":
    root.merge(home)
    root.mount('/auth', auth)
    root.mount('/app', dashboard)
    root.run(host='0.0.0.0', port=8080, debug=True, reloader=True)

