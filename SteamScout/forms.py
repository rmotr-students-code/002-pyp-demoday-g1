from flask_wtf import Form
from wtforms.validators import Required, Length, Email, EqualTo, NumberRange
from wtforms import (TextField, PasswordField, BooleanField, IntegerField, DecimalField,
                     RadioField)


class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    remember_me = BooleanField('remember_me', default=False) 


class SignUpForm(Form):
    username = TextField('Enter a Username', validators= [
            Length(min=4, max=25, 
            message=(u'You\'re username must be between 4 and 25 characters')),
            Required("Please enter a username")])
               
    email = TextField('Enter Your Email', validators= [
            Required("Please enter a valid email address"), 
            Email(message=(u'That\'s not a valid email address'))])
            
    password = PasswordField('Enter a Password', validators= [
            Required("Enter a secure password"), 
            EqualTo('confirm', message=(u'Passwords must match'))])
               
    confirm = PasswordField('Please Repeat your Password', validators= [
            Required("Please repeat your password")])
     
     
class PercentPref(Form):
    threshold_percent = IntegerField('percent threshold', validators=[Required("Please enter a number between 1-100"),
                           
                                                                      NumberRange(min=1, max=100)])
class AmountPref(Form):
    threshold_amount = DecimalField('amount threshold', validators=[Required("Please enter an amount between .01 and 1000.00"),
                       
                                                                    NumberRange(min=.01, max=1000.0)])
class GamesSearch(Form):
    search_term = TextField('Enter a Game', validators=[Required("Please enter a game to search for")])