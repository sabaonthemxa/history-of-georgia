from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, length

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if not field.data.lower().endswith("@gmail.com"):
            raise ValidationError("Only Gmail addresses (@gmail.com) are allowed.")

class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=6)])
    submit = SubmitField("Login")

