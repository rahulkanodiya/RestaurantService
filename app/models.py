from app import db
from flask import url_for

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)    
    description = db.Column(db.String(120))
    address = db.Column(db.String(120))
    contact = db.Column(db.String(15), index=True)
    table = db.relationship('Table', backref='owner', lazy='dynamic')
    menu = db.relationship('Menu', backref='owner', lazy='dynamic')    

    def __repr__(self):
        return '<Restaurant name {}  Id {}>'.format(self.name, self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'description': self.description,
            'address': self.address,
            'contact': self.contact,
            '_links': {                    
            'self': url_for('api.restaurant', id=self.id),
            'menus': url_for('api.menus', id=self.id),
            'tables': url_for('api.tables', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'email', 'description', 'address', 'contact']:
            setattr(self, field, data[field])

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    description = db.Column(db.String(120))
    menu_type = db.Column(db.String(30))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))    

    def to_dict(self):
        data = {
            'id': self.id,
            'description': self.description,
            'menu_type': self.menu_type,
            'restaurant': self.owner.name,
            '_links': {
                'self': url_for('api.menu', id=self.restaurant_id, menu_id=self.id),
                'restaurant': url_for('api.restaurant', id=self.restaurant_id)                
                }
            }
        return data

    def from_dict(self, data):
        if 'name' in data:
            restaurant = Restaurant.query.filter_by(name=data['name']).first()
            if restaurant:
                setattr(self, 'restaurant_id', restaurant.id)
                for field in ['description', 'menu_type']:
                    if field in data:
                        setattr(self, field, data[field])
            else:
                setattr(self, 'restaurant_id', 0)                
        else:
            setattr(self, 'restaurant_id', 0)


class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    number = db.Column(db.Integer, index=True)
    capacity = db.Column(db.Integer)
    booked = db.Column(db.Boolean, default=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    def to_dict(self):
        data = {
            'id': self.id,
            'number': self.number,            
            'capacity': self.capacity,
            'booked': self.booked,
            'restaurant': self.owner.name,
            '_links': {
                'self': url_for('api.table', id=self.restaurant_id, table_id=self.id),
                'restaurant': url_for('api.restaurant', id=self.restaurant_id)                
                }
            }
        return data

    def from_dict(self, data):
        if 'name' in data:
            restaurant = Restaurant.query.filter_by(name=data['name']).first()
            if restaurant:
                setattr(self, 'restaurant_id', restaurant.id)
                for field in ['number', 'capacity']:
                    if field in data:
                        setattr(self, field, data[field])
            else:
                setattr(self, 'restaurant_id', 0)                
        else:
            setattr(self, 'restaurant_id', 0)
