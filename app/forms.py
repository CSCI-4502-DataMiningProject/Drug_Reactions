from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

COUNTRY_CODES = [
    (11, 'AU'),
    (6, 'CA'),
    (8, 'CH'),
    (5, 'CN'),
    (9, 'CO'),
    (4, 'DE'),
    (13, 'ES'),
    (3, 'GB'),
    (10, 'IT'),
    (7, 'JP'),
    (12, 'RO'),
    (2, 'TR'),
    (1, 'US'),
    (14, 'Other')
]

class NBForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120, message="Enter an age between 0 and 120")])
    weight = IntegerField('Weight', validators=[DataRequired(), NumberRange(min=0, max=400, message="Enter a weight between 0 and 400")])
    country = SelectField('Country', choices=COUNTRY_CODES, coerce=int)
    is_male = BooleanField('Patient is Male')
    submit = SubmitField('Calculate Probability')
