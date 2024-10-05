import sys
sys.path.append('app')

from models import User, Session, Post, db_login
from core.http import render_template, MyHandler
from http.cookies import SimpleCookie
import os


def login(request: MyHandler):
    context = {}
    code = 200
    if request.command == "POST":
        register_keys = ("email", "password")
        data = request.form_data
        if all([key in register_keys for key in data]):
            response, code = db_login(
                **{key: data[key] for key in register_keys})
            if code == None:
                cookie = SimpleCookie()
                cookie["session"] = response['session_token']
                cookie['session']['path'] = '/'
                cookie['session']['httponly'] = True
                request.send_response(302)
                request.send_header(
                    'Set-Cookie', cookie.output(header='', sep='').strip())
                request.send_header('Location', '/posts')
                request.end_headers()
                return
            else:
                context = response
        else:
            context = {"error": "fill all the inputs"}

    request.send_response(code)
    request.send_header('Content-type', 'text/html')
    request.end_headers()
    request.wfile.write(render_template(
        'app/templates/login.html', context).encode())


def post(request: MyHandler):
    session_cookie = request.cookies.get("session")
    user = None
    post_id = request.query_data.get("id")
    if session_cookie:
        session_token = session_cookie.value
        user = Session.get_user(session_token)

    if not user:
        request.send_response(302)
        request.send_header('Location', '/')
        request.end_headers()
        return
    if not post_id:
        request.send_error(404, "post doesnt exist")
        return
    if request.command == "POST":
        post_body = request.form_data.get("text")
        Post.add_post(user.id, post_body, post_id)

    context = Post.get_post_by_id(post_id)
    request.send_response(200)
    request.send_header('Content-type', 'text/html')
    request.end_headers()
    request.wfile.write(render_template(
        'app/templates/post.html', context).encode())


def posts(request: MyHandler):
    session_cookie = request.cookies.get("session")
    user = None
    if session_cookie:
        session_token = session_cookie.value
        user = Session.get_user(session_token)

    if not user:
        request.send_response(302)
        request.send_header('Location', '/')
        request.end_headers()
        return
    if request.command == "POST":
        post_body = request.form_data.get("text")
        Post.add_post(user.id, post_body)

    posts = Post.get_posts()
    context = {"posts": posts}
    request.send_response(200)
    request.send_header('Content-type', 'text/html')
    request.end_headers()
    request.wfile.write(render_template(
        'app/templates/posts.html', context).encode())


def register(request: MyHandler):
    context = {}
    if request.command == "POST":
        register_keys = ("name", "email", "password1", "password2")
        data = request.form_data
        if all([key in register_keys for key in data]):
            context = User.add_user(
                **{key: data[key] for key in register_keys})
            if not context:
                request.send_response(302)
                request.send_header('Location', '/login')
                request.end_headers()
                return
        else:
            context = {"error": "fill all the inputs"}

    request.send_response(200)
    request.send_header('Content-type', 'text/html')
    request.end_headers()
    request.wfile.write(render_template(
        'app/templates/register.html', context).encode())


def index(request: MyHandler):
    request.send_response(200)
    request.send_header('Content-type', 'text/html')
    request.end_headers()
    request.wfile.write(render_template('app/templates/index.html').encode())

def static(request:MyHandler):
    file_path = request.path.lstrip('/')
    full_path = os.path.join("app/templates", file_path)
    if os.path.exists(full_path):
            if full_path.endswith(".css"):
                content_type = "text/css"
            elif full_path.endswith(".jpg"):
                content_type = "image/jpeg"

            with open(full_path, 'rb') as f:
                request.send_response(200)
                request.send_header('Content-type', content_type)
                request.end_headers()
                request.wfile.write(f.read())
    else:
        request.send_error(404, "File not found")