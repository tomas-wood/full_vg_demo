from app import app
from gevent.pywsgi import WSGIServer
if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0',threaded=True)
    http_server = WSGIServer(('0.0.0.0',5000), app)
    http_server.serve_forever()

