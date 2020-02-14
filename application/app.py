##################### Imports #####################

from flask import Flask, request, abort, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from application import config
from werkzeug.utils import secure_filename
from bson import ObjectId
from logging.handlers import RotatingFileHandler
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, \
    jwt_required, jwt_optional, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
import pymongo
import datetime
import logging
import json
import os


##################### Initialize #####################

app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)
mongo = PyMongo(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

blacklist = set()


##################### logging part #####################

my_logger = logging.getLogger('waitress')
logging.basicConfig(filename='log/info.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
my_logger.addHandler(logging.handlers.RotatingFileHandler('log/info.log', maxBytes=1000000, backupCount=20))


@app.before_request
@jwt_optional
def before_request():
    if get_jwt_identity():
        app.logger.info('Request with method: %s for the uri %s from the user %s .', request.method, request.path, get_jwt_identity())
    else:
        app.logger.info('Request with method: %s for the uri %s .', request.method, request.path)


##################### Test part #####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/start')
@jwt_optional
def start():
    if get_jwt_identity():
        return hello_world()
    else:
        return jsonify(msg="It is neccesary to be logged."), 401


##################### login part #####################

@app.route('/login', methods=['GET'])
def login():
    try:
        username=request.authorization["username"]
        password=request.authorization["password"]
    except Exception as e:
        app.logger.warning('Exception: no username or password in Basic authorization header.')
        return jsonify(error="Unauthenticated. Not basic auth send with username or password."), 401

    from application.models import Users, Projects
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
                access_token=accesstoken,
                refresh_token=refreshtoken
                )
        else:
            return jsonify(
                username=username,
                email=user.email,
                project="none",
                project_description="",
                access_token=accesstoken,
                refresh_token=refreshtoken
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
    return jsonify(msg= "Successfully logged out.")


@app.route('/changepassword', methods=['PUT'])
@jwt_required
def changepassword():
    try:
        newpassword=request.headers['newpassword']
    except Exception as e:
        app.logger.warning("Exception. The newpassword is not in the headers.")
        return jsonify(error="Error. The newpassword is not in the headers."), 400

    from application.models import Users
    user = Users.query.filter_by(username=get_jwt_identity()).first()
    if user is not None:
        user.password = newpassword
        db.session.commit()
        app.logger.info('%s changed password successfully.', get_jwt_identity())
        return jsonify(msg="Password change successfully."), 200
    else:
        app.logger.warning("Unauthenticated. Error in the token.")
        return jsonify(error="Unauthenticated. Error in the token."), 401


##################### dmps part #####################

# DMP format: { "user":"esteban","project":"street-spectra", "purpose":"collection of elements", "sharing":yes, "license":"cc-by"}

@app.route('/dmps', methods=['GET'])
@jwt_required
def get_all_dmps():
    dmps = mongo.db.dmps.find({'user': get_jwt_identity()})
    output = []
    for dmp in dmps:
        output.append(dmp)
    app.logger.info('%s received dmps successfully.', get_jwt_identity())
    return JSONEncoder().encode(output)


@app.route('/dmps', methods=['POST'])
@jwt_required
def post_dmp():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        app.logger.warning("Failed to decode JSON object.")
        return jsonify(error="Failed to decode JSON object."), 400
    data.update({'user':get_jwt_identity()})
    _id = mongo.db.dmps.insert_one(data).inserted_id
    app.logger.info('dmp %s generated by %s successfully.', str(_id), get_jwt_identity())
    return jsonify({'id':str(_id), 'ok': True, 'msg': 'DMP created successfully.'}), 201 


@app.route('/dmps/<dmp_id>', methods=['GET'])
@jwt_required
def get_dmp(dmp_id):
    try:
        dmp = mongo.db.dmps.find_one({'_id': ObjectId(dmp_id)})
    except Exception as e:
        app.logger.warning("Not a correct dmp id.")
        return jsonify(error="Not a correct dmp id."), 400
    if dmp is None:
        app.logger.warning('DMP %s not found.', dmp_id)
        return jsonify({'error': 'DMP ' + dmp_id + 'not found.'}), 404
    app.logger.info('%s received %s dmp successfully.', get_jwt_identity(), dmp_id)
    return JSONEncoder().encode(dmp)


@app.route('/dmps/<dmp_id>', methods=['PUT'])
@jwt_required
def put_dmp(dmp_id):
    try:
        data = request.get_json(force=True)
    except Exception as e:
        app.logger.warning("Failed to decode JSON object.")
        return jsonify(error="Failed to decode JSON object."), 400
    data.update({'user':get_jwt_identity()})
    try:
        success = mongo.db.dmps.update({"_id": ObjectId(dmp_id), 'user': get_jwt_identity()}, {"$set": data})
    except Exception as e:
        app.logger.warning("Not a correct dmp id: %s .", dmp_id)
        return jsonify(error="Not a correct dmp id."), 400
    if success.get('updatedExisting') is False:
        app.logger.info('dmp %s of the user %s not found.', dmp_id, get_jwt_identity())
        return jsonify({'ok': False, 'msg': 'DMP of the user '+ get_jwt_identity() + ' not found.'})
    app.logger.info('dmp %s updated by %s successfully.', dmp_id, get_jwt_identity())
    return jsonify({'id':dmp_id, 'ok': True, 'msg': 'DMP updated successfully.'})


@app.route('/dmps/<dmp_id>', methods=['DELETE'])
@jwt_required
def delete_dmp(dmp_id):
    try:
        success = mongo.db.dmps.delete_one({'_id': ObjectId(dmp_id), 'user': get_jwt_identity()})
    except Exception as e:
        app.logger.warning("Not a correct dmp id: %s for this user %s .", dmp_id, get_jwt_identity())
        return jsonify(error="Not a correct dmp id."), 400
    if success.deleted_count == 0:
        app.logger.info('dmp %s of the user %s not found.', dmp_id, get_jwt_identity())
        return jsonify({'ok': False, 'msg': 'DMP of the user '+ get_jwt_identity() + ' not found.'})
    app.logger.info('dmp %s delete by %s successfully.', dmp_id, get_jwt_identity())
    return jsonify({'id':dmp_id, 'ok': True, 'msg': 'DMP delete successfully.'})


##################### tasks part #####################

## Format task = {status, url, dmp}
## Stauts: pending, finished, error
## Example: {"status":"pending", "url":"nothingYet", "dmp":"1234"}

@app.route('/tasks', methods=['GET'])
@jwt_required
def get_all_tasks():
    id_dmp = request.args.get('id_dmp')
    status = request.args.get('status')
    if id_dmp is not None:
        if status is not None:
            tasks = mongo.db.tasks.find({'dmp':id_dmp,'status':status}).sort('timestamp',pymongo.DESCENDING)
        else:
            tasks = mongo.db.tasks.find({'dmp':id_dmp}).sort('timestamp',pymongo.DESCENDING)
    else:
        if status is not None:
            tasks = mongo.db.tasks.find({'status':status}).sort('timestamp',pymongo.DESCENDING)
        else:
            tasks = mongo.db.tasks.find().sort('timestamp',pymongo.DESCENDING)
    output = []
    for task in tasks:
        output.append(task)
    app.logger.info('%s received tasks successfully.', get_jwt_identity())
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
    data.update({'timestamp':datetime.datetime.utcnow()})
    _id = mongo.db.tasks.insert_one(data).inserted_id
    app.logger.info('task %s created by %s successfully.', str(_id), get_jwt_identity())
    return jsonify({'id':str(_id), 'ok': True, 'msg': 'Task created successfully.'}), 201


@app.route('/tasks/<task_id>', methods=['GET'])
@jwt_required
def get_task(task_id):
    try:
        tasks = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    except Exception as e:
        app.logger.warning("Not a correct tasks id.")
        return jsonify(error="Not a correct tasks id."), 400
    if tasks is None:
        app.logger.warning('Task %s not found.', task_id)
        return jsonify({'error': 'Task ' + task_id + 'not found.'}), 404
    app.logger.info('%s received %s task successfully.', get_jwt_identity(), task_id)
    return JSONEncoder().encode(tasks)


##################### File part #####################

@app.route('/resources/docx/<file_id>', methods=['GET'])
@jwt_optional
def return_files_docx(file_id):
    try:
        app.logger.info("User %s require document %s .", get_jwt_identity(), file_id)
        return send_from_directory('../documents', filename= file_id,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            attachment_filename='dmp.docx',
            as_attachment=True,
            cache_timeout=0)
    except Exception as e:
        app.logger.warning("Failed to send the %s file to %s.", file_id, get_jwt_identity())
        return jsonify(error="Failed to send the docx file."), 400


@app.route('/resources/pdf/<file_id>', methods=['GET'])
@jwt_optional
def return_files_pdf(file_id):
    try:
        app.logger.info("User %s require document %s .", get_jwt_identity(), file_id)
        return send_from_directory('../documents', filename= file_id,
            mimetype='application/pdf',
            attachment_filename='dmp.pdf',
            as_attachment=True,
            cache_timeout=0)
    except Exception as e:
        app.logger.warning("Failed to send the %s file to %s.", file_id, get_jwt_identity())
        return jsonify(error="Failed to send the pdf file."), 400
    

##################### Tokens JWT part #####################

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    app.logger.info('%s refresh his token successfully.', get_jwt_identity())
    return jsonify(access_token= create_access_token(identity=get_jwt_identity())), 201


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


##################### Error handler part #####################

@app.errorhandler(404)
@jwt_optional
def page_not_found(error):
    if get_jwt_identity():
        app.logger.error('Page not found. Method: %s uri: %s user: %s', request.method, request.path, get_jwt_identity())
        return jsonify({'error':"Page not found..."}), 404
    else:
        app.logger.error('Page not found. Method: %s uri: %s', request.method, request.path)
        return jsonify({'error':"Page not found..."}), 404

@app.errorhandler(401)
@jwt_optional
def unauthorized(error):
    if get_jwt_identity():
        app.logger.error('Unauthorized. Method: %s uri: %s user: %s', request.method, request.path, get_jwt_identity())
        return jsonify({'error':"Unauthorized"}), 404
    else:
        app.logger.error('Unauthorized. Method: %s uri: %s', request.method, request.path)
        return jsonify({'error':"Unauthorized."}), 401

@app.errorhandler(405)
@jwt_optional
def method_not_allowed(error):
    if get_jwt_identity():
        app.logger.error('Method not allowed. Method: %s uri: %s user: %s', request.method, request.path, get_jwt_identity())
        return jsonify({'error':"Method not allowed."}), 404
    else:
        app.logger.error('Method not allowed. Method: %s uri: %s', request.method, request.path)
        return jsonify({'error':"Method not allowed."}), 401


##################### Resources (class) #####################

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
