import datetime
from main import *
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/api/heart_rate", methods=["POST"])
def user_data():
    r = request.get_json()
    email = r["user_email"]
    age = r["user_age"]
    hr = r["heart_rate"]
    try:
        user = add_heart_rate(email, hr, time=datetime.datetime.now())
    except:
        user = create_user(email, age, hr, time=datetime.datetime.now())
        return "User data created."
    return "User data updated."


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def user_heart_rate(user_email):
    try:
        hr = {
            "heart_rate": hr_data(user_email)
        }
        return jsonify(hr)
    except:
        return "User does not exist."


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def user_avg_heart_rate(user_email):
    try:
        average = {
            "average_heart_rate": hr_avg(user_email)
        }
        return jsonify(average)
    except:
        return "User does not exist."


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def user_int_avg():
    try:
        r = request.get_json()
        email = r["user_email"]
        ref_time = r["heart_rate_average_since"]
        d = interval_data(email, ref_time)
        int_avg = {
            "interval average since time": d[0],
            "tachycardia status": d[1]
        }
        return jsonify(int_avg)
    except:
        return "User does not exist."
