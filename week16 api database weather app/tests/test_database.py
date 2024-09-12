from database import WeatherDatabase
import sys
import pytest
import sqlite3
from datetime import datetime, timedelta
sys.path.append("../")


@pytest.fixture
def weather_db():
    db = WeatherDatabase()
    return db


def test_save_request_data(weather_db):
    city_name = "London"
    request_time = datetime.now().isoformat()
    weather_db.save_request_data(city_name, request_time)

    connection = sqlite3.connect(weather_db.db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT city, time FROM request;")
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    assert result == (city_name, request_time)


def test_save_response_data(weather_db):

    city_name = "London"
    request_time = datetime.now().isoformat()
    weather_db.save_request_data(city_name, request_time)

    response_data = {
        "name": city_name,
        "temp": 15.0,
        "feels_like": 13.0,
        "last_updated_time": datetime.now().isoformat()
    }

    weather_db.save_response_data(response_data)
    connection = sqlite3.connect(weather_db.db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT city, temperature, feels_like, last_update FROM response;")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    assert result == (response_data["name"], response_data["temp"],
                      response_data["feels_like"], response_data["last_updated_time"])


def test_get_request_count(weather_db):

    weather_db.save_request_data("London", datetime.now().isoformat())
    weather_db.save_request_data("Paris", datetime.now().isoformat())

    count = weather_db.get_request_count()

    assert count == 2


def test_get_successful_request_count(weather_db):
    city_name = "London"
    request_time = datetime.now().isoformat()
    weather_db.save_request_data(city_name, request_time)
    response_data = {
        "name": city_name,
        "temp": 15.0,
        "feels_like": 13.0,
        "last_updated_time": datetime.now().isoformat()
    }
    weather_db.save_response_data(response_data)
    count = weather_db.get_successful_request_count()
    assert count == 1


def test_get_last_hour_requests(weather_db):
    weather_db.save_request_data(
        "London", (datetime.now() - timedelta(minutes=30)).isoformat())
    weather_db.save_request_data(
        "Paris", (datetime.now() - timedelta(hours=2)).isoformat())
    last_hour_requests = weather_db.get_last_hour_requests()
    assert len(last_hour_requests) == 1
    assert last_hour_requests[0][0] == "London"


def test_get_city_request_count(weather_db):
    weather_db.save_request_data("London", datetime.now().isoformat())
    weather_db.save_request_data("Paris", datetime.now().isoformat())
    weather_db.save_request_data("London", datetime.now().isoformat())
    city_request_counts = weather_db.get_city_request_count()
    assert city_request_counts == [("London", 2), ("Paris", 1)]
