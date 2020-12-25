from flask_wtf import FlaskForm
from datetime import *
# 这两个import用于设置输入, 和限制文件的类型; 这个FileAllowed是个validator;
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Todo.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                         validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                              validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError("This username has already been taken")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError("This email has already been taken")
   

class LoginForm(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                              validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                         validators=[DataRequired(), Email()])
    
    # 设置picture的字段, 用于后续的更新照片;
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


    # 这些自定义验证函数的基本格式是: validate_fieldname(self, field), FlaskForm为根据函数名自动匹配对应的字段;
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError("This username has already been taken")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError("This email has already been taken")


class TodoForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    deadline = DateField('Deadline', validators = [DataRequired()])
    submit = SubmitField('Post')

    # 防止ddl设置在当前日期之前
    def validate_deadline(self, deadline):
        today = date.today()

        if today > deadline.data:
            raise ValidationError("Deadline can't be set before today !")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user is None:
            raise ValidationError("There is no account with that email, you must register first !")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                              validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')