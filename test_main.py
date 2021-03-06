import pytest
import datetime
from main import *


def test_user():
    email = "testuser32@gmail.com"
    age = 20
    heart_rate = 60
    time = datetime.datetime(2018, 3, 23, 0, 0, 0, 000000)
    return [email, age, heart_rate, time]


def test_user2():
    email = "testuser12@gmail.com"
    age = 12
    heart_rate = 100
    time = datetime.datetime(2018, 3, 23, 0, 0, 0, 000000)
    return [email, age, heart_rate, time]


def test_create_user():
    u = test_user()
    create_user(u[0], u[1], u[2], u[3])
    time = datetime.datetime(2018, 3, 23, 0, 0, 0, 000000)
    user = models.User.objects.raw({"_id": "testuser32@gmail.com"}).first()
    assert user.email == "testuser32@gmail.com"
    assert user.age == 20
    assert user.heart_rate == [60]
    assert user.heart_rate_times == [time]


def test_add_heart_rate():
    u = test_user()
    create_user(u[0], u[1], u[2], u[3])
    time1 = datetime.datetime(2018, 3, 23, 0, 0, 0, 000000)
    time2 = datetime.datetime(2018, 3, 23, 0, 2, 0, 000000)
    add_heart_rate(u[0], 80, datetime.datetime(2018, 3, 23, 0, 2, 0, 000000))
    user = models.User.objects.raw({"_id": "testuser32@gmail.com"}).first()
    assert user.heart_rate == [60, 80]
    assert user.heart_rate_times == [time1, time2]


def test_hr_data():
    u = test_user()
    create_user(u[0], u[1], u[2], u[3])
    add_heart_rate(u[0], 80, datetime.datetime(2018, 3, 23, 0, 2, 0, 000000))
    add_heart_rate(u[0], 70, datetime.datetime(2018, 3, 23, 0, 4, 0, 000000))
    add_heart_rate(u[0], 120, datetime.datetime(2018, 3, 23, 0, 6, 0, 000000))
    assert hr_data(u[0]) == [60, 80, 70, 120]


def test_hr_avg():
    u = test_user()
    create_user(u[0], u[1], u[2], u[3])
    add_heart_rate(u[0], 80, datetime.datetime(2018, 3, 23, 0, 2, 0, 000000))
    add_heart_rate(u[0], 70, datetime.datetime(2018, 3, 23, 0, 4, 0, 000000))
    add_heart_rate(u[0], 120, datetime.datetime(2018, 3, 23, 0, 6, 0, 000000))
    assert hr_avg(u[0]) == pytest.approx(82.5, 0.1)


def test_interval_data():
    u = test_user()
    create_user(u[0], u[1], u[2], u[3])
    ref_time1 = "2018-03-23 00:05:00.0000"
    actual1 = [pytest.approx(130, 0.1), "Present."]
    add_heart_rate(u[0], 80, datetime.datetime(2018, 3, 23, 0, 2, 0, 000000))
    add_heart_rate(u[0], 70, datetime.datetime(2018, 3, 23, 0, 4, 0, 000000))
    add_heart_rate(u[0], 120, datetime.datetime(2018, 3, 23, 0, 6, 0, 000000))
    add_heart_rate(u[0], 140, datetime.datetime(2018, 3, 23, 0, 8, 0, 000000))
    add_heart_rate(u[0], 130, datetime.datetime(2018, 3, 23, 0, 10, 0, 000000))
    assert interval_data(u[0], ref_time1) == actual1

    u2 = test_user2()
    create_user(u2[0], u2[1], u2[2], u[3])
    ref_time2 = "2018-03-23 00:05:00.0000"
    actual2 = [pytest.approx(123.3, 0.1), "Not present."]
    add_heart_rate(u2[0], 140, datetime.datetime(2018, 3, 23, 0, 2, 0, 000000))
    add_heart_rate(u2[0], 120, datetime.datetime(2018, 3, 23, 0, 4, 0, 000000))
    add_heart_rate(u2[0], 120, datetime.datetime(2018, 3, 23, 0, 6, 0, 000000))
    add_heart_rate(u2[0], 160, datetime.datetime(2018, 3, 23, 0, 8, 0, 000000))
    add_heart_rate(u2[0], 90, datetime.datetime(2018, 3, 23, 0, 10, 0, 000000))
    assert interval_data(u2[0], ref_time2) == actual2
