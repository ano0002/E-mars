from datetime import timedelta
import os, typing, time


from flask import Flask, flash, redirect, url_for, request, session, make_response, jsonify, render_template


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from forms.upload_score import UploadScoreForm

app = Flask(__name__)


if os.getenv('DATABASE_URL'):
    uri = os.getenv('DATABASE_URL')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
else:
    uri = 'postgresql://mbxxmdmigtirnd:d637b19fb11b4e602ab652dcb3fee791221f56bf2d40c624e9f58a076bd8732e@ec2-52-72-56-59.compute-1.amazonaws.com:5432/d6gd48d1vqjbv6'   




app.config['FLASK_ENV'] = 'production'
app.config['TESTING'] = False
app.secret_key = 'suezeazezaeza'
app.SECRET_KEY = 'suezeazezaeza'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.permanent_session_lifetime = timedelta(minutes=20)
app.app_context().push()
from data import db

from data import Data



db.init_app(app)
db.create_all()
DataBase = Data()

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)


@app.errorhandler(405)
def error_405(e) -> make_response:
    return make_response(jsonify({"error": "405 Method Not Allowed"}), 405)


@app.errorhandler(404)
def error_404(e) -> make_response:
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/", methods=["GET",])
@limiter.limit("1000/day;100/hour;10/minute")
def hello_world():
    return make_response(jsonify({"status": "online"}), 200)


@app.route("/api/upload_score", methods=["POST",])
def upload_score():
    form = UploadScoreForm()
    if form.validate_on_submit():
        #uploads the score of the user to the database
        user = DataBase.get_user(form.username.data)
        if user is None:
            return make_response(jsonify({'error': 'User not found'}), 404)
        user_id = user.id
        score = form.score.data
        DataBase.upload_score(user_id=user_id, score=score)
        return make_response(jsonify({'status': 'ok'}), 200)
