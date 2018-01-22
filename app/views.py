# -*- coding: utf-8 -*-

from flask import jsonify

from app import app
from app.auth import requires_authorization
from app.db_upload import DbUpload
from .extract import Extraction


@app.route('/', methods=['GET'])
@app.route('/api/v1.0/pets', methods=['GET'])
def get_tasks():
    extraction = Extraction()
    pets = extraction.extract("http://www.schronisko-zwierzaki.lublin.pl")

    return jsonify({'cats': pets[0], 'dogs': pets[1]})


@app.route('/db', methods=['GET'])
@requires_authorization
def start_db_upload():
    db_upload = DbUpload()
    db_upload.run()

    message = 'DB upload successful'
    return message
