import weather as w
import re
import pytest

def test_my_ip():
    test_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", w.my_ip()).group()
    assert  w.my_ip() == test_ip


def test_my_location():
    assert len(w.my_location("145.40.146.248")) == 3
    assert len(w.my_location("8.8.8.8")) == 3


def test_get_latlon():
    assert len(w.get_latlon("New York")) == 3
    assert len(w.get_latlon("Southampton")) == 3


def test_check_weatcher():
    assert len(w.check_weather(1, 1, 1)) == 4


def test_show_forecast():
    assert w.show_forecast("Monday", 0, 25.5, 30.2) == " Monday: :sun:  Clear sky. Temperatures ranging from 25.5°C to 30.2°C."
    assert w.show_forecast("😀", "😀", "😀", "😀") == " 😀: :sleeping_face:  Unavailable. Temperatures ranging from 😀°C to 😀°C."
    assert w.show_forecast("", "", "", "") == " : :sleeping_face:  Unavailable. Temperatures ranging from °C to °C."


def test_convert_code():
    assert w.convert_code(61) == ":cloud_with_rain:  Rain: Slight, moderate and heavy intensity"
    assert w.convert_code(200) == ":sleeping_face:  Unavailable"
    assert w.convert_code("cat") == ":sleeping_face:  Unavailable"


def test_errors():
    with pytest.raises(SystemExit):
        w.get_latlon("Hawaigh")

    with pytest.raises(SystemExit):
        w.get_latlon("")

    with pytest.raises(SystemExit):
        w.check_weather("","","")

    with pytest.raises(SystemExit):
        w.check_weather("1","1","-1")

    with pytest.raises(SystemExit):
        w.my_location("8.8.8")

    with pytest.raises(SystemExit):
        w.my_location("cat")

