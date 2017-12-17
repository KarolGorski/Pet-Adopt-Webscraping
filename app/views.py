# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect
from app import app
from .forms import *
from .extract import Extraction
from flask import request
from flask import send_file
from flask import jsonify


@app.route('/todo/api/v1.0/pets', methods=['GET'])
def get_tasks():
        
    extraction = Extraction()
    pets = extraction.extract("http://www.schronisko-zwierzaki.lublin.pl")
    return jsonify({'pets': pets})
