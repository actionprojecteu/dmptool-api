from flask import Flask, render_template, redirect, url_for, request, abort,\
    session, jsonify
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
import os

import json
from bson import ObjectId
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)
mongo = PyMongo(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/start')
def start():
    if current_user.is_authenticated:
        return redirect(url_for("hello_world"))
    else:
        return jsonify(
                message="It is neccesary to be logged."
                )

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return jsonify(
            message="User already logged: " + current_user.username
            )

    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=request.authorization["username"]).first()
    if user is not None and user.verify_password(request.authorization["password"]):
        session.permanent = True
        login_user(user)
        return jsonify(
            username=request.authorization["username"],
            email=user.email
            )
    else:
        return jsonify(error="Unauthenticated. Error in log in."), 401

@app.route("/logout")
def logout():
    logout_user()
    return jsonify(
                message="User has logout."
                )

@app.route('/changepassword/')
@login_required
def changepassword():
    if not current_user.is_authenticated:
            return jsonify(error="Unauthenticated. Error in log in."), 401

    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=current_user.username).first()
    if user is not None:
        user.password = request.headers['newpassword']
        db.session.commit()
        return jsonify(
            message="Password change successfully"
            )
    else:
        return jsonify(error="Unauthenticated. Error in log in."), 401


########## Esteban part ##########

@app.route('/dmps', methods=['GET'])
@login_required
def get_all_dmps():
    dmps = mongo.db.dmps.find()
    output = []

    for dmp in dmps:
        output.append(dmp)

    print (output)
    return JSONEncoder().encode(output)

#{ "user":"esteban","project":"street-spectra", "purpose":"collection of elements", "sharing":yes, "license":"cc-by"}

@app.route('/dmps', methods=['POST'])
@login_required
def post_dmp():
    data = request.get_json()

    mongo.db.dmps.insert_one(data)

    return jsonify({'ok': True, 'message': 'DMP created successfully!'}), 200


@app.route('/dmps/<dmp_id>', methods=['PUT'])
@login_required
def put_dmp(dmp_id):
    data = request.get_json()

    mongo.db.dmps.update_one({"name": dmp_id}, {"$set": data})

    return jsonify({'ok': True, 'message': 'DMP updated successfully!'}), 200


########## Login manager part ##########

@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error':"Unauthorized. You need to log in first."})

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error':"Page not found..."}), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error':"Unauthorized"}), 401
