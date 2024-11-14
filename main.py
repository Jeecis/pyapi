#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
import redis
import uuid

app = Flask(__name__)

# Synchronous Redis client
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

@app.route('/', methods=['GET'])
def get_simple():
    return "The server is running"


# Add a new record to Redis
@app.route('/add_record', methods=['POST'])
def add_record():
    record_data = json.loads(request.data)
    name = record_data.get('name')
    data = record_data.get('data')

    if not name or not data:
        return jsonify({"error": "Invalid input"}), 400

    record_id = str(uuid.uuid4()) 

    try:
        redis_client.set(record_id, str({"name": name, "data": data}))
    except Exception:
        return jsonify({"Error": "error occurred while reading REDIS entries"}), 500

    return jsonify({"message": "Record added successfully", "record": record_data}), 201


@app.route('/delete_record', methods=['DELETE'])
def delete_record():
    record_data = json.loads(request.data)
    id = record_data.get('id')

    if not id:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        redis_client.delete(id)
    except Exception:
        return jsonify({"Error": "error occurred while deleting an entry"}), 500

    return jsonify({"message": "Record deleted successfully"}), 200

@app.route('/get_record', methods=['GET'])
def get_record():
    record_data = json.loads(request.data)
    id = record_data.get('id')

    try:
        record = redis_client.get(id)
    except Exception:
        return jsonify({"Error": "error occurred while reading REDIS entry"}), 500
    
    record_json_str = record.replace("'", '"')
    record_json = json.loads(record_json_str)

    return jsonify(record_json)


@app.route('/get_all_records', methods=['GET'])
def get_all_records():
    records_list = []

    try:
        keys = redis_client.keys()
    except Exception:
        return jsonify({"Error": "error occurred while reading REDIS entries"}), 500
    
    for key in keys:

        try:
            record = redis_client.get(key)
        except Exception:
            return jsonify({"Error": "error occurred while reading REDIS entries"}), 500
        
        record_json_str = record.replace("'", '"')
        record_json = json.loads(record_json_str)
        records_list.append({key:record_json})


    return jsonify(records_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
