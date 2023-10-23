from app import app
from flask import render_template, request, redirect, send_from_directory

from web.use_cases.staff import *
from web.use_cases.consumables import *
from web.use_cases.salaries import *
from web.use_cases.services import *
from web.use_cases.bonuses import *
from web.use_cases.departments import *
from web.use_cases.roles import *
from web.use_cases.payouts import *
from web.use_cases.traffic import *


@app.route('/', methods=['GET', ])
def new_page():
    return render_template(
        'index.html'
    )


@app.route('/archive', methods=['GET', ])
def archieve():
    return render_template(
        'archive.html'
    )


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static', filename)
