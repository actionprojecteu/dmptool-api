import json
from bson import ObjectId
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["MONGO_URI"] = "uri_mongo"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dmps', methods=['GET'])
def get_all_dmps():
    dmps = mongo.db.dmptool.find()
    output = []

    for dmp in dmps:
        output.append(dmp)

    print (output)
    return JSONEncoder().encode(output)

#{ "user":"esteban","project":"street-spectra", "purpose":"collection of elements", "sharing":yes, "license":"cc-by"}

@app.route('/dmps', methods=['POST'])
def post_dmp():
    data = request.get_json()

    mongo.db.dmptool.insert_one(data)

    return jsonify({'ok': True, 'message': 'DMP created successfully!'}), 200


@app.route('/dmps/<dmp_id>', methods=['PUT'])
def put_dmp(dmp_id):
    data = request.get_json()

    mongo.db.dmptool.update_one({"name": dmp_id}, {"$set": data})

    return jsonify({'ok': True, 'message': 'DMP updated successfully!'}), 200

if __name__ == '__main__':
    app.run()