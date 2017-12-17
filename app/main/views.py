import json
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash
from flask_login import current_user, login_required
from . import main
from datetime import datetime
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
    typelist = tblType.query.all()
    try:
        ed = datetime.strptime(form.enddate.data,'%Y-%m-%d %H:%M:%S')
    except:
        ed = None
    if request.method == 'POST':
        print(request.form.get('id'))
        if request.form.get('id'):
            print('update')
            inputdata = tblData.query.get(request.form.get('id'))
            inputdata.startdate=form.startdate.data
            inputdata.enddate = ed
            inputdata.address = form.address.data
            inputdata.area = form.area.data
            inputdata.type_id = form.type_id.data
            inputdata.user_id = current_user.id
        else:
            print('add')
            inputdata=tblData(startdate=form.startdate.data,
            enddate=ed,
            address=form.address.data,
            area=form.area.data,
            type_id=form.type_id.data,
            user_id=current_user.id)
        db.session.add(inputdata)
        flash('输入信息成功')
        return redirect(url_for('main.addData'))
    return render_template('add.html',form=form, typelist=typelist)

@main.route('/tblJSON/')
@login_required
def tblJSON():
    """
    逆序、分页查询停水信息列表，JSON格式
    """
    return '''{"code":0,"msg":"","count":%d,"data":%s}''' %(tblData.query.count(), tblData.query.order_by(db.desc(tblData.id)).offset(int(request.args.get('limit'))*(int(request.args.get('page'))-1)).limit(request.args.get('limit')).all())
