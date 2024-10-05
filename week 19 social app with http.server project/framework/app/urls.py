from . import views

urlpatterns = (
    {"path":"/", "view":views.index },
    {"path":"/login", "view":views.login},
    {"path":"/register", "view":views.register},
    {"path":"/post", "view":views.post},
    {"path":"/posts", "view":views.posts},
    {"path":"/css/style.min.css", "view":views.static},
    {"path":"/img/showcase.jpg", "view":views.static},
)