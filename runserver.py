from app import app
# from werkzeug.serving import run_simple
from wsgiref.simple_server import make_server

if __name__ == '__main__':
    httpd = make_server('0.0.0.0', 5000, app)
    httpd.serve_forever()
