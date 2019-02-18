from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired

from models import Store

class RegisterStore(Form):
	store_name = StringField(
		'Storename',
		validators=[
			DataRequired()
		]
	)