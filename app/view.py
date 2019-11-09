import os
import json
import random
from collections import defaultdict
from uuid import uuid4
from app import app
from app.controller import custom_error
from flask import (
    jsonify,
    request,
    Response,
    render_template,
    make_response,
    abort,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


app.url_map.converters["regex"] = RegexConverter
PATH_STATIC_RESOUCES = f"{os.path.dirname(os.path.abspath(__file__))}/static/"
PATH_TEMPLATE_RESOUCES = f"{os.path.dirname(os.path.abspath(__file__))}/templates/"
SBADMIN2 = "sbadmin2"
USER_DATA = "user_data.json"


def import_data():
    user_data = defaultdict(dict)
    try:
        with open(USER_DATA, "r") as fp:
            _data = json.load(fp)
            user_data.update(_data)

    except Exception:
        print(f"Failed to import data {USER_DATA}.")

    return user_data


def save_data(data):
    data_to_save = import_data()
    try:
        idx = data.pop("ID") if "ID" in data else str(uuid4())
        data_to_save[idx] = {k.lower(): v for k, v in data.items()}
        with open(USER_DATA, "w") as fw:
            json.dump(data_to_save, fw)

    except Exception as e:
        print(f"Failed to save data {USER_DATA}.")

    return data_to_save


def delete_data(uuid):
    data_to_save = import_data()
    try:
        data_to_save.pop(uuid)
        with open(USER_DATA, "w") as fw:
            json.dump(data_to_save, fw)

    except KeyError:
        print(f"Failed to delete {uuid} from data {USER_DATA}.")

    return data_to_save


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


# For default templates
@app.route(r"/<regex(r'[\w-]+\.html'):file>")
def send_static_html(file):
    return send_from_directory(os.path.join(PATH_TEMPLATE_RESOUCES, SBADMIN2), file)


@app.route("""/regex/<regex("[abcABC0-9]{4,6}"):uid>-<slug>/""")
def example_regex(uid, slug):
    return "uid: %s, slug: %s" % (uid, slug)


@app.route("/index")
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


@app.route("/coaches", methods=["GET", "POST", "DELETE"])
def manage_users():
    # # mock data
    # data = [
    #     {
    #         "id": "12345",
    #         "name": "Stanley",
    #         "position": "TW",
    #         "office": "Pentium",
    #         "age": "30",
    #         "date": "2019-09-08 10:00:00",
    #         "salary": "100K",
    #     }
    # ] * 100
    # return render_template("/sbadmin2/tables.html", data=data)
    user_data = import_data()
    users = list()
    for idx, v in user_data.items():
        v.update(id=idx)
        users.append(v)

    return render_template("/sbadmin2/tables.html", data=users)


# FIXME: Until find the way to pass submitted data
# @app.route("/users", methods=["POST"])
# def create_user():
#     body = get_request_body(request)
#     print(body, type(body))
#     return handle_general_page(body)

# FIXME: Until find the way to pass submitted data
# @app.route("/users/<path:user_id>", methods=["PUT"])
# def update_user(user_id):
#     body = get_request_body(request)
#     print("update", user_id)
#     print(body, type(body))
#     return handle_general_page({"id": user_id})


@app.route("/createuser", methods=["POST"])
def create_user():
    body = get_request_body(request)
    save_data(body)
    return redirect("/tables")


@app.route("/updateuser", methods=["POST"])
def update_user():
    body = get_request_body(request)
    save_data(body)
    return redirect("/tables")


@app.route("/users/<path:user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted_data = delete_data(user_id)
    return deleted_data or {}


@app.route("/judger", methods=["GET"])
def count_users():
    user_data = import_data()
    users = list()
    for idx, v in user_data.items():
        if "name" in v:
            users.append(v["name"])
        else:
            continue

    population_size = (len(users) // 100) * 10 ** 5
    sampling = random.choices(users, k=population_size)
    counts = list()
    score = 0
    winner = None
    for user in users:
        hits = sampling.count(user)
        counts.append(hits)
        if hits > score:
            winner = user
            score = hits

    return render_template(
        "/sbadmin2/charts.html", users=users, counts=counts, winner=winner
    )


def get_request_body(request, is_json=True):
    if request.content_type == "application/x-www-form-urlencoded":
        body = request.form.to_dict()
        return body

    body = request.get_data()
    if is_json:
        try:
            body = json.loads(body)
        except json.JSONDecodeError as e:
            body = body.decode("UTF-8")
    else:
        body = body.decode("UTF-8")

    return body


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
