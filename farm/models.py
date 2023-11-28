#!/usr/bin/env python3
"""Models"""

from config import db, ma

class Product(db.Model):
    """Product class"""

    __tablename__ = 'product'
    p_id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.Text) 
    price = db.Column(db.Float, nullable=False) 
    available = db.Column(db.Boolean, default=True) 
    image = db.Column(db.String(150)) 

    def __repr__(self):
        return f"<Product(name={self.name!r})>"
  
class CartItem(db.Model):
    """Cart class"""

    __tablename__ = 'cartitem'
    c_id = db.Column(db.Integer, primary_key=True) 
    product_id = db.Column(db.Integer, db.ForeignKey('product.p_id')) 
    quantity = db.Column(db.Integer, default=1) 

    def __repr__(self):
        return f"<Cart(name={self.name!r})>"
    

class ProductSchema(ma.SQLAlchemySchema):
    """Product schema"""

    class Meta:
        """Product metadata"""

        model = Product
        load_instance = True

    p_id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    price = ma.auto_field()
    available = ma.auto_field()
    image = ma.auto_field()

class CartSchema(ma.SQLAlchemySchema):
    """Cart schema"""

    class Meta:
        """Cart metadata"""

        model = CartItem
        load_instance = True

    c_id = ma.auto_field()
    product_id = ma.auto_field()
    quantity = ma.auto_field()