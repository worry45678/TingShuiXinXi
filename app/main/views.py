import json
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash
from flask_login import current_user, login_required
from . import main

from .. import db
from .forms import InputData
from ..models import tblData, tblType, tblUser



@main.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@main.route('/add', methods=['GET','POST'])
@login_required
def addData():
    form = InputData()
    if form.validate_on_submit():
        inputdata = tblData(startdate=form.startdate.data,
        enddate = form.enddate.data,
        address=form.address.data,
        area=form.area.data,
        type_id=form.type_id.data,
        user_id=current_user.id)
        db.session.add(inputdata)
        flash('输入信息成功')
        return redirect(url_for('main.addData'))
    return render_template('add.html',form=form)

