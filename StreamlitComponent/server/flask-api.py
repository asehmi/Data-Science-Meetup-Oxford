import sys
import flask
import time

app = flask.Flask(__name__)

@app.route('/api/ping', methods=['GET'])
def ping():
    result = {f'ping': f'{time.asctime(time.localtime(LAST_REQUEST_SEC))}'}
    return result

LAST_REQUEST_SEC = 0
@app.before_request
def update_last_request_ms():
    global LAST_REQUEST_SEC
    LAST_REQUEST_SEC = time.time()

@app.after_request
def after_request(response):
    # If the request comes from a sandboxed iframe, the origin will be
    # the string "null", which is not covered by the "*" wildcard.
    # To handle this, we set "Access-Control-Allow-Origin: null".
    response.headers.add(
        "Access-Control-Allow-Origin",
        "null" if flask.request.origin == "null" else "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

if __name__ == '__main__':
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
        app.run(port=PORT, use_reloader=False)
    else:
        app.run(use_reloader=False)
