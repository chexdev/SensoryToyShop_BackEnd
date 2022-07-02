# import database (db)
from . import db


# Product Category (Table)
class ProductCategory(db.Model):
    __tablename__ = 'productCategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False,
                      default='defaultproductCategory.jpg')
    products = db.relationship('Product', backref='ProductCategory',
                               cascade="all, delete-orphan")  # one-to-many, composition rship

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}\n"
        str = str.format(self.id, self.name, self.description, self.image)
        return str


# Order Details (Table)
orderdetails = db.Table('orderdetails',
                        db.Column('order_id', db.Integer, db.ForeignKey(
                            'orders.id'), nullable=False),
                        db.Column('product_id', db.Integer, db.ForeignKey(
                            'products.id'), nullable=False),
                        db.PrimaryKeyConstraint('order_id', 'product_id'))  # primary key constraint, 2 foreign keys


#Product (Table)
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    productCategory_id = db.Column(
        db.Integer, db.ForeignKey('productCategories.id'))  # one-to-one rship

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}, Price: {}, Product Category: {}, Date: {}\n"
        str = str.format(self.id, self.name, self.description,
                         self.image, self.price, self.productCategory_id, self.date)
        return str


#ProductInfo (Table)
class ProductInfo(db.Model):
    __tablename__ = 'productInfo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'))  # one-to-one rship

    def __repr__(self):
        str = "Id: {}, Description: {}, Product: {}\n"
        str = str.format(self.id, self.description,
                         self.product_id)
        return str


#Order (Table)
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    # status True = order checked out
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    products = db.relationship(
        "Product", secondary=orderdetails, backref="orders")  # one-to-many rship

    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Date: {}, Products: {}, Total Cost: {}\n"
        str = str.format(self.id, self.status, self.firstname, self.surname,
                         self.email, self.phone, self.date, self.products, self.totalcost)
        return str
