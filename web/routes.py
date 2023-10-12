from app import app
from flask import render_template, request, redirect

from web.use_cases.staff import *
from web.use_cases.consumables import *
from web.use_cases.salaries import *
from web.use_cases.services import *
from web.use_cases.bonuses import *
from web.use_cases.departments import *
from web.use_cases.roles import *
from web.use_cases.payouts import *


@app.route('/', methods=['GET', ])
def new_page():
    return render_template(
        'index.html'
    )
