from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=15)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)],
        render_kw={"placeholder": "Email"},
    )
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=15)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Sign up")
