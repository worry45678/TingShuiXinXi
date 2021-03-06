from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, logout_user, login_required, current_user #flask_login 中管理用户登陆的函数
from ..models import tblUser
from .. import db
from .forms import LoginForm,RegistrationForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    登陆页面
    """
    form = LoginForm()
    if request.method == 'POST': # 验证是否提交按钮
        user = tblUser.query.filter_by(name=form.username.data).first() # 数据库中获取username对应的对象
        if user is not None and user.verify_password(form.password.data): # 验证用户名和密码
            login_user(user, form.remember_me.data) # 使用login_user函数登陆用户
            return redirect(request.args.get('next') or url_for('main.index'))  # 登陆成功，返回index页面或跳转页面
        flash('账号或密码错误') # 否则返回密码账号或密码错误
    return render_template('auth/login.html', form=form) # 登陆失败，返回login页面


@auth.route('/logout')
@login_required
def logout():
    logout_user() # 使用login_user函数登出用户 
    return redirect(url_for('main.index')) # 登出成功，返回index页面

@auth.route('/serect')
@login_required # 保护路由，非登陆用户返回login页面,且使用next参数传递当前页面地址，登陆后直接跳转当前地址
def secret():
    return 'Only authenticated users are allowed!'


@auth.route('/register', methods=['GET','POST'])
def register():
    """
    注册页面，根据用户表单填写信息写入数据库，已有用户返回flash错误信息
    """
    form = RegistrationForm()
    if request.method == 'POST':
        if tblUser.query.filter_by(name=form.username.data):
            flash('该用户名已注册，请直接登录')
            return render_template('auth/register.html', form=form)
        else:
            user = tblUser(name=form.username.data, password=form.password.data)
            db.session.add(user)
            flash('You can now login')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)