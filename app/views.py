# -*- coding: utf-8 -*-

from flask import jsonify

from app import app
from .extract import Extraction

@app.route('/', methods=['GET'])
@app.route('/api/v1.0/pets', methods=['GET'])
def get_tasks():
        
    extraction = Extraction()
    pets = extraction.extract("http://www.schronisko-zwierzaki.lublin.pl")
    return jsonify({'pets': pets})
