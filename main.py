#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_simple():
    
    return "Wussup"

@app.route('/wussup', methods=['GET'])
def get_wussup():
    
    return "Wussup g"

@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    return jsonify(record)
    

app.run(host="0.0.0.0", port=5000)