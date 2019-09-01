import os
from app import app
from app.controller import custom_error
from flask import (
    jsonify,
    render_template,
    make_response,
    abort,
    redirect,
    url_for,
    send_from_directory,
)


PATH_STATIC_RESOUCES = f"{os.path.dirname(os.path.abspath(__file__))}/static/"
SBADMIN2 = "sbadmin2"
os.path.join(PATH_STATIC_RESOUCES, SBADMIN2)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        PATH_STATIC_RESOUCES, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@app.route("/css/<path:path>")
def send_static_css(path):
    return send_from_directory(
        os.path.join(PATH_STATIC_RESOUCES, SBADMIN2, "css"), path
    )


@app.route("/js/<path:path>")
def send_static_js(path):
    return send_from_directory(os.path.join(PATH_STATIC_RESOUCES, SBADMIN2, "js"), path)


@app.route("/img/<path:path>")
def send_static_img(path):
    return send_from_directory(
        os.path.join(PATH_STATIC_RESOUCES, SBADMIN2, "img"), path
    )


@app.route("/vendor/<path:path>")
def send_static_vendor(path):
    return send_from_directory(
        os.path.join(PATH_STATIC_RESOUCES, SBADMIN2, "vendor"), path
    )


@app.route("/")
def index():
    title = "Chapter 0: Start Page"
    body = "Welcome passengers. Ready to set sail."
    return render_template("index.html", title=title, body=body)


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/home")
def home():
    return render_template("/sbadmin2/index.html")


def handle_general_page(response):
    response = jsonify(response)
    response.headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }
    return response


@app.errorhandler(custom_error)
def handle_custom_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.code
    response.headers = error.headers
    return response


@app.errorhandler(401)
def handle_unauthorized(error):
    title = "Chapter 401: The Unauthorized Page"
    body = (
        "Your ticket does not seem to be valid or expired"
        " and therefore cannot be passed."
    )
    return render_template("errorpage.html", title=title, body=body), 401


@app.errorhandler(403)
def handle_permission_denied(error):
    title = "Chapter 403: The Forbidden Page"
    body = (
        "This ship is sailing to a region which is forbidden and dangerous, be careful."
    )
    return render_template("errorpage.html", title=title, body=body), 403


@app.errorhandler(404)
def handle_path_not_found(error):
    title = "Chapter 404: The Lost Page"
    body = (
        "A careful and diligent search has been made for the desired page,"
        " but it just cannot be found."
    )
    return render_template("errorpage.html", title=title, body=body), 404


@app.errorhandler(500)
def handle_internal_server_error(error):
    title = "Chapter 500: The Unexpected Page"
    body = (
        "We are facing an unexpected circumstance and so sorry for the inconvenience."
    )
    return render_template("errorpage.html", title=title, body=body), 500
