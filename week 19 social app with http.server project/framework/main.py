from core.http import run_server
from app.urls import urlpatterns

if __name__ == "__main__":
    # Start the web server and pass the urlpatterns for URL routing
    run_server(urlpatterns)
