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
    try:
        ed = datetime.strptime(form.enddate.data,'%Y-%m-%d %H:%M:%S')
    except:
        ed = None
    if request.method == 'POST':
        inputdata=tblData(startdate=form.startdate.data,
        enddate=ed,
        address=form.address.data,
        area=form.area.data,
        type_id=form.type_id.data,
        user_id=current_user.id)
        db.session.add(inputdata)
        flash('输入信息成功')
        return redirect(url_for('main.addData'))
    return render_template('add.html',form=form)

@main.route('/tblJSON/')
@login_required
def tblJSON():
    return '''{"code":0,"msg":"","count":8,"data":%s}''' %tblData.query.all()

@main.route('/tblJSON2')
@login_required
def tblJSON2():
    return '''{"code":0,"msg":"","count":1000,"data":[{"id":10000,"username":"user-0","sex":"女","city":"城市-0","sign":"签名-0","experience":255,"logins":24,"wealth":82830700,"classify":"作家","score":57},{"id":10001,"username":"user-1","sex":"男","city":"城市-1","sign":"签名-1","experience":884,"logins":58,"wealth":64928690,"classify":"词人","score":27},{"id":10002,"username":"user-2","sex":"女","city":"城市-2","sign":"签名-2","experience":650,"logins":77,"wealth":6298078,"classify":"酱油","score":31},{"id":10003,"username":"user-3","sex":"女","city":"城市-3","sign":"签名-3","experience":362,"logins":157,"wealth":37117017,"classify":"诗人","score":68},{"id":10004,"username":"user-4","sex":"男","city":"城市-4","sign":"签名-4","experience":807,"logins":51,"wealth":76263262,"classify":"作家","score":6},{"id":10005,"username":"user-5","sex":"女","city":"城市-5","sign":"签名-5","experience":173,"logins":68,"wealth":60344147,"classify":"作家","score":87},{"id":10006,"username":"user-6","sex":"女","city":"城市-6","sign":"签名-6","experience":982,"logins":37,"wealth":57768166,"classify":"作家","score":34},{"id":10007,"username":"user-7","sex":"男","city":"城市-7","sign":"签名-7","experience":727,"logins":150,"wealth":82030578,"classify":"作家","score":28},{"id":10008,"username":"user-8","sex":"男","city":"城市-8","sign":"签名-8","experience":951,"logins":133,"wealth":16503371,"classify":"词人","score":14},{"id":10009,"username":"user-9","sex":"女","city":"城市-9","sign":"签名-9","experience":484,"logins":25,"wealth":86801934,"classify":"词人","score":75}]}'''