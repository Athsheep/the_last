#-*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'保持登陆')
    submit = SubmitField(u'登陆')
    
class RegistrationForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'账户名', validators=[Required(), Length(1, 64), 
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'字母数字和下划线')])
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message=u'密码必须匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册' )
    

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'账户名已注册')
            

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册')
                
class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message=u'密码必须匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')
    
class PasswordResetRequestForm(Form):
    email = StringField(u'邮箱', validators=[Required()])
    submit = SubmitField(u'提交')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱不存在.')
    
class PasswordResetForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message=u'密码必须匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')
    
class ChangeEmailForm(Form):
    email = StringField(u'新邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'提交')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册')