from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField#, RadioField, SelectField
from wtforms.validators import InputRequired, email

# form used in basket


class CheckoutForm(FlaskForm):
    first_name = StringField(
        "Your first name", default="Nathan", validators=[InputRequired()])
    last_name = StringField(
        "Your surname", default="Eshraghi", validators=[InputRequired()])
    email = StringField("Your email", default="nathan@gmail.com",
                        validators=[InputRequired(), email()])
    phone = StringField("Your phone number",
                        default="0475465231", validators=[InputRequired()])
    submit = SubmitField("Checkout")


# class ShippingChoice(FlaskForm):
#     shipping_choice = SelectField(u'Choose your shipping', choices=[(
#         'standard', 'Standard Postage ($9.95)'), ('express', 'Express Postage ($15.95)')], default='standard'
#     )
