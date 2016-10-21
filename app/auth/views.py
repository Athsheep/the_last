#-*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, \
    PasswordResetForm, ChangeEmailForm
from ..models import User
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'账户或密码不正确')  
    return render_template('auth/login.html', form=form)
    
    
@auth.route('/logout', methods=['GET', 'POST'])
def logout():   
    logout_user()
    flash(u'已退出')
    return redirect(url_for('main.index'))
    
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'confirm email', 'auth/email/confirm', user=user, token=token)
        flash(u'注册成功！请登录邮箱确认注册。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
    
    
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        
        return redirect(url_for('main.index'))
        
    if current_user.confirm(token):
        flash(u'感谢通过确认')
        
    else:
        flash(u'链接无效，请重发邮件确认')
    return redirect(url_for('main.index'))   


        
        
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
   
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
    
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(user.email, 'confirm email', 'auth/email/confirm', user=current_user, token=token)
    flash(u'确认邮件已发送至邮箱')
    return redirect(url_for('main.index'))
    
@auth.route('/change-password', methods=['GET', 'POST'])    
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'密码已更改')
            return redirect(url_for('main.index'))
        else:    
            flash(u'密码错误')
            
    return render_template("auth/change_password.html", form=form)    
            
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, u'重设密码', 'auth/email/reset_password', user=user, token=token, 
                        next=request.args.get('next'))
        flash(u'重设密码的邮件已发送到邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)    
    
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(u'密码已经重置')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))    
    return render_template('auth/reset_password.html', form=form)       
 
 
@auth.route('/change-email', methods=['GET', 'POST']) 
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, u'确认邮箱地址', 'auth/email/change_email', user=current_user, token=token)
            flash(u'确认新邮箱的邮件已发送到你的邮箱')
            return redirect(url_for('main.index'))
        else:
            flash(u'邮箱或密码错误')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'你的邮箱已更新')
    else:
        flash(u'请求错误')
    return redirect(url_for('main.index'))
    
        