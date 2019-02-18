import peeweedbevolve
from flask import (Flask, render_template, request, flash, redirect, url_for)
from models import db, Store, Warehouse, Product

# python -c 'import os; print(os.urandom(16))'
# b'_5#y2L"F4Q8z\n\xec]/

app = Flask(__name__)
app.secret_key = 'secret_key!'

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

@app.route("/contact")
def contact():
	return render_template('contact.html')

@app.route("/store", methods=['GET', 'POST'])
def store():
	# form = forms.Store()
	if request.method == 'POST':
		# How to post a success message from form submission if not using flash but using bootstrap under 'store.html' line 5
		# breakpoint()
		new_store = Store(name=request.form['store_name'])
		new_store.save()
		flash("Store created", "success")
		return redirect(url_for('store'))
	else:
		return render_template('store.html')

@app.route("/warehouse", methods=['GET', 'POST'])
def warehouse():
	store_list = Store.select()
	if request.method == 'POST':
		# How to post a success message from form submission if not using flash but using bootstrap under 'store.html' line 5
		# breakpoint()
		store = Store.get_by_id(request.form['store_id'])
		new_warehouse = Warehouse(location=request.form['warehouse_location'], store=store)
		new_warehouse.save()
		flash("Warehouse created", "success")
		return redirect(url_for('warehouse'))
	else:
		return render_template('warehouse.html', store_list=store_list)

if __name__ == '__main__':
	app.run()