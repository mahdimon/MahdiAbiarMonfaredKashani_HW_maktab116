from functools import cached_property
import http.cookies
import http.server
from jinja2 import Environment, FileSystemLoader
from core.routing import resolve
from urllib.parse import urlparse, parse_qsl
import os


class MyHandler(http.server.BaseHTTPRequestHandler):

    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return http.cookies.SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        view_func = resolve(self.url.path)
        if view_func:
            view_func(self)
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        self.do_GET()


def run_server(urlpatterns):
    PORT = 8000
    with http.server.HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()


def render_template(template_name, context={}):
    template_dir = os.path.join(os.getcwd())
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(context)
