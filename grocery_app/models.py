from sqlalchemy_utils import URLType
from sqlalchemy.orm import backref
from flask_login import UserMixin, current_user 
from grocery_app.extensions import db
from grocery_app.utils import FormEnum

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    def __str__(self):
        return f'<Grocery Store: {self.title}>'

    def __repr__(self):
        return f'<Grocery Store: {self.title}>'

class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(URLType)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users_who_added = db.relationship(
        'User', secondary='user_item', back_populates='shopping_list')
    

    def __str__(self):
        return f'<Grocery Item: {self.name}>'

    def __repr__(self):
        return f'<Grocery Item: {self.name}>'

class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=True)
    shopping_list = db.relationship(
        'GroceryItem', secondary='user_item', back_populates='users_who_added')

    def __str__(self):
        return f'<User: {self.username}>'

    def __repr__(self):
        return f'<User: {self.username}>'

shopping_list_table = db.Table('user_item',
    db.Column('item_id', db.Integer, db.ForeignKey('grocery_item.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)