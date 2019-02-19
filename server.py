import peeweedbevolve
from flask import (Flask, render_template, request, flash, redirect, url_for)
from models import db, Store, Warehouse, Product
from peewee import *

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
	# store_list = Store.select()
	store_list = Store.select()
	payload = []
	for store in store_list:
		new_object = {
			"store_name": store.name,
			"num": len(list(store.warehouses))
		}
		payload.append(new_object)
	if request.method == 'POST':
		# How to post a success message from form submission if not using flash but using bootstrap under 'store.html' line 5
		# breakpoint()
		new_store = Store(name=request.form['store_name'])
		new_store.save()
		flash("Store created", "success")
		return redirect(url_for('store'), store_list)
	else:
		return render_template('store.html', payload=payload)

@app.route("/store/<int:store_number>", methods=['GET', 'POST'])
def store_info(store_number):
	if request.method == 'POST':
		new_store_name = request.form['new_store_name']
		Store.update({Store.name: new_store_name}).where(Store.id == store_number)
		return redirect(url_for('store/index'))
	else:
		store_id = Store.select().where(Store.id == store_number)
		num_of_wh = True
		for store in store_id:
			num_of_wh = len(list(store.warehouses))
		return render_template('store_page.html', store_id=store_id, num_of_wh=num_of_wh)

@app.route("/warehouse", methods=['GET', 'POST'])
def warehouse():
	if request.method == 'POST':
		store = request.form['store_list']
		location = request.form['warehouse_location']
		new_warehouse = Warehouse.create(location=location, store=store)
		new_warehouse.save()
		flash("Warehouse created", "success")
		return redirect(url_for('warehouse'))
	else:
		# result = Store.select(Store.name, fn.COUNT(Warehouse.store.id == Store.id)).join(Warehouse).group_by(Store.name).where(Store.id == Warehouse.store.id)
		warehouse_list = Warehouse.select()
		store_list = Store.select()
		return render_template('warehouse.html', warehouse_list=warehouse_list, store_list=store_list)

@app.route("/product", methods=['GET', 'POST'])
def product():
	if request.method == 'POST':
		name = request.form['product_name']
		description = request.form['product_description']
		warehouse = request.form['warehouse_list']
		color = request.form['product_color']
		new_product = Product(name=name, description=description, warehouse=warehouse, color=color)
		new_product.save()
		flash("Product created", "success")
		return redirect(url_for('product'))
	else:
		product_list = Product.select()
		warehouse_list = Warehouse.select()
		return render_template('product.html', warehouse_list=warehouse_list, product_list=product_list)

if __name__ == '__main__':
	app.run()