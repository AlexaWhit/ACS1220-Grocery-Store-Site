import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, ItemCategory, User
from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm, UserForm 
from flask_login import login_user, logout_user, login_required, current_user

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           MAIN Routes                  #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    all_users = User.query.all()
    return render_template('home.html', 
        all_stores=all_stores, all_users=all_users)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()

    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
        )
        db.session.add(new_store)
        db.session.commit()
    
        flash(f'Success! {new_store.title} was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()

    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category =form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
        )
        db.session.add(new_item)
        db.session.commit()

        flash(f'Success! {new_item.name} was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # STRETCH CHALLENGE: Fill out the Create User route
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            username =form.username.data,
        )
        db.session.add(user)
        db.session.commit()

        flash(f'Success! {user.username} was created successfully.')
        return redirect(url_for('main.homepage'))

    return render_template('create_user.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    # STRETCH - Add delete capability
    if form.delete.data:
        return redirect(url_for('main.delete_store', store_id=store.id)) 

    if form.validate_on_submit():
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()

        flash(f'Good News! {store.title} was UPDATED successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)

    # STRETCH - Add delete capability
    if form.delete.data:
        return redirect(url_for('main.delete_item', item_id=item.id)) 

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()

        flash(f'Good News! {item.name} was UPDATED successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('item_detail.html', item=item, form=form)

@main.route('/delete/<item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = GroceryItem.query.get(item_id)
    # Stretch - delete the item
    try:
        db.session.delete(item)
        db.session.commit()
        flash(f'Successfully deleted {item.name}'.format(item))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')

@main.route('/profile/<username>')
@login_required
def profile(username):
    # TODO: Make a query for the user with the given username, and send to the
    # template
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('profile.html', user=user)
    else:
        flash('User not found!')
        return redirect(url_for('main.homepage')) 

@main.route('/add_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)

    if item not in current_user.shopping_list:
        current_user.shopping_list.append(item)
        db.session.commit()
        flash(f'Success! {item.name} has been ADDED to your shopping list!')  
        return redirect(url_for('main.item_detail', item_id=item.id)) 
    else:   
        return "ERROR!"

@main.route('/remove_shopping_list/<item_id>', methods=['POST'])
@login_required
def remove_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)

    if item in current_user.shopping_list:
        current_user.shopping_list.remove(item)
        db.session.commit()
        flash(f'Success! {item.name} has been REMOVED from your favorites!')   
        return redirect(url_for('main.item_detail', item_id=item.id)) 
    else:   
        return "ERROR!"

