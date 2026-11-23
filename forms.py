
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    remember = BooleanField("Remember me")

    submit = SubmitField("Login")


class NoteForm(FlaskForm):
    title = StringField(
        "Note Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    category = StringField(
        "Category",
        validators=[
            Length(max=50)
        ]
    )

    content = TextAreaField(
        "Note Content",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Note")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
