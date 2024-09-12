#scorce https://opensource.com/article/21/9/unit-test-python
import sys
sys.path.append("../")
import json
import pytest
from http import HTTPStatus

from weather_server import get_city_weather
@pytest.fixture()
def fake_weather_info():
    """Fixture that returns a static weather data."""
    return {
    "name": "London",
    "main": {
        "temp": 15.0,
        "feels_like": 13.0,
    },
    "dt": 1694536800
}


def test_get_city_weather_using_mocks(mocker, fake_weather_info):
    """Given a city name, test that a HTML report about the weather is generated
    correctly."""

    # Create a fake requests response object
    fake_resp = mocker.Mock()

    # Mock the json method to return the static weather data
    fake_resp.json = mocker.Mock(return_value=fake_weather_info)

    # Mock the status code
    fake_resp.status_code = HTTPStatus.OK

    # Mock the requests.get function to return the fake response
    mocker.patch("weather_server.requests.get", return_value=fake_resp)

    # Call the retrieve_weather function with the city name
    weather_info = get_city_weather("London")

    # Assert that the returned weather info matches the expected data
    assert weather_info == {"name": "London", "temp": 15.0, "feels_like": 13.0, "last_updated_time": "2023-09-12 20:10:00"}


