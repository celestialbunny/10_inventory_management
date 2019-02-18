import peeweedbevolve
from flask import (Flask, render_template, request, flash)
from models import db, Store, Warehouse, Product

app = Flask(__name__)

@app.before_request
def before_request():
	db.connect()

@app.after_request
def after_request(response):
	db.close()
	return response

@app.cli.command()
def migrate():
	db.evolve(ignore_tables={'base_model'})

'''
Start of the own declared directory
'''

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/store", methods=['GET', 'POST'])
def store():
	# form = forms.Store()
	flash("hi", "success")
	if request.method == 'POST':
		# How to post a success message from form submission if not using flash but using bootstrap under 'store.html' line 5
		# breakpoint()
		store1 = Store(name=request.form['store_name'])
		store1.save()

	return render_template('store.html')

if __name__ == '__main__':
	app.run()