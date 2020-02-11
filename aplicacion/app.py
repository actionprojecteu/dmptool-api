################# Imports #################
from flask import Flask, request, abort, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from werkzeug.utils import secure_filename
from bson import ObjectId
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, \
    jwt_required, jwt_optional, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
import os
import json
import logging


################# Initialize #################

app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)
mongo = PyMongo(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

blacklist = set()

logging.basicConfig(filename='log/info.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/start')
@jwt_optional
def start():
    if get_jwt_identity():
        return hello_world()
    else:
        return jsonify(message="It is neccesary to be logged."), 401


################# login part #################

@app.route('/login', methods=['GET'])
def login():
    if get_jwt_identity() is not None:
        return jsonify(message="User already logged: " + get_jwt_identity())

    try:
        username=request.authorization["username"]
        password=request.authorization["password"]
    except Exception as e:
            app.logger.warning('Exception: no username or password in Basic authorization header.')
            return jsonify(error="Unauthenticated. Not basic auth send with username or password."), 401

    from aplicacion.models import Users, Projects
    user = Users.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        accesstoken = create_access_token(identity = username)
        refreshtoken = create_refresh_token(identity = username)
        app.logger.info('%s logged in successfully.', user.username)

        # userprojects = Projects.query.filter(Projects.users.any(id=user.id)).all()
        # nameprojects=""
        # for i,project in enumerate(userprojects):
        #     nameprojects+=project.name
        #     if i < len(userproject) - 1:
        #         nameprojects+=","
        userproject = Projects.query.filter(Projects.users.any(id=user.id)).first()

        if userproject is not None:
            return jsonify(
                username=username,
                email=user.email,
                project=userproject.name,
                project_description=userproject.description,
                access_token= accesstoken,
                refresh_token= refreshtoken
                )
        else:
            return jsonify(
                username=username,
                email=user.email,
                project="none",
                project_description="",
                access_token= accesstoken,
                refresh_token= refreshtoken
                )
    else:
        app.logger.warning("Unauthenticated. Error in log in.")
        return jsonify(error="Unauthenticated. Error in log in."), 401


@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    app.logger.info('%s logged out successfully.', get_jwt_identity())
    return jsonify(message= "Successfully logged out.")


@app.route('/changepassword', methods=['PUT'])
@jwt_required
def changepassword():
    try:
        newpassword=request.headers['newpassword']
    except Exception as e:
        app.logger.warning("Exception. The newpassword is not in the headers.")
        return jsonify(error="Error. The newpassword is not in the headers."), 400

    from aplicacion.models import Users
    user = Users.query.filter_by(username=get_jwt_identity()).first()
    if user is not None:
        user.password = newpassword
        db.session.commit()
        app.logger.info('%s changed password successfully.', get_jwt_identity())
        return jsonify(message="Password change successfully."), 200
    else:
        app.logger.warning("Unauthenticated. Error in the token.")
        return jsonify(error="Unauthenticated. Error in the token."), 401


################# dmps part #################

# DMP format: { "user":"esteban","project":"street-spectra", "purpose":"collection of elements", "sharing":yes, "license":"cc-by"}

@app.route('/dmps', methods=['GET'])
@jwt_required
def get_all_dmps():
    dmps = mongo.db.dmps.find({'user': get_jwt_identity()})
    output = []
    for dmp in dmps:
        output.append(dmp)
    return JSONEncoder().encode(output)


@app.route('/dmps', methods=['POST'])
@jwt_required
def post_dmp():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        app.logger.warning("Failed to decode JSON object.")
        return jsonify(error="Failed to decode JSON object."), 400
    _id = mongo.db.dmps.insert_one(data).inserted_id
    return jsonify({'id':str(_id), 'ok': True, 'message': 'DMP created successfully.'}), 201 


@app.route('/dmps/<dmp_id>', methods=['GET'])
@jwt_required
def get_dmp(dmp_id):
    try:
        dmp = mongo.db.dmps.find_one({'_id': ObjectId(dmp_id)})
    except Exception as e:
        app.logger.warning("Not a correct dmp id format.")
        return jsonify(error="Not a correct dmp id format."), 400
    if dmp is None:
        return jsonify({'error': 'DMP ' + dmp_id + 'not found.'}), 404
    return JSONEncoder().encode(dmp)


@app.route('/dmps/<dmp_id>', methods=['PUT'])
@jwt_required
def put_dmp(dmp_id):
    try:
        data = request.get_json(force=True)
    except Exception as e:
        app.logger.warning("Failed to decode JSON object.")
        return jsonify(error="Failed to decode JSON object."), 400
    try:
        mongo.db.dmps.update({"_id": ObjectId(dmp_id)}, {"$set": data})
    except Exception as e:
        print(e)
        return jsonify(error="Not a correct dmp id format."), 400
    return jsonify({'ok': True, 'message': 'DMP updated successfully.'})


################# tasks part #################

## Format task = {status, url, dmp}
## Stauts: pending, finished, error
## Example: {"status":"pending", "url":"nothingYet", "dmp":"1234"}

@app.route('/tasks', methods=['GET'])
@jwt_required
def get_all_tasks():
    status = request.args.get('status')
    if status is not None:
        tasks = mongo.db.tasks.find({'status':status})
    else:
        tasks = mongo.db.tasks.find()
    output = []
    for task in tasks:
        output.append(task)
    return JSONEncoder().encode(output)

@app.route('/tasks', methods=['POST'])
@jwt_required
def post_task():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        app.logger.warning("Failed to decode JSON object.")
        return jsonify(error="Failed to decode JSON object."), 400
    data.update({'status':'pending'})
    _id = mongo.db.tasks.insert_one(data).inserted_id
    return jsonify({'id':str(_id), 'ok': True, 'message': 'Task created successfully.'}), 201


################# Tokens JWT part #################

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    return jsonify(access_token= create_access_token(identity=get_jwt_identity())), 201

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


################# Error handler part #################

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error':"Page not found..."}), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error':"Unauthorized."}), 401


################# Resources (class) #################

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
