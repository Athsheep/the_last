#-*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField(u'帐户名', validators=[Required()])
    submit = SubmitField(u'登陆')
    
class EditProfileForm(Form):
    name = StringField(u'名字', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'文章')
    submit = SubmitField(u'提交')
    
class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'账户名', validators=[Required(), Length(1, 64),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'字母数字和下划线')])
    confirmed = BooleanField(u'确认状态')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Required()])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.id).all()]
        self.user = user
        
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册')
                
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'账户名已被注册')
            
            
class PostForm(Form):
    body = PageDownField(u'我想说', validators=[Required()])
    submit = SubmitField(u'提交')
    
class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField(u'提交')
    
