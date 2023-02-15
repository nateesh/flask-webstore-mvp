from . import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        str = "ID: {}     Name: {}"
        str = str.format(self.id, self.name)
        return str


orderdetails = db.Table('orderdetails',
                        db.Column('book_id', db.ForeignKey('books.id'),
                                  nullable=False, primary_key=True),
                        db.Column('order_id', db.ForeignKey('orders.id'), nullable=False, primary_key=True))


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    author = db.Column(db.String(128), unique=True)
    isbn = db.Column(db.String(32), unique=True)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, nullable=False)
    num_ratings = db.Column(db.Integer)
    image = db.Column(db.String(60), nullable=False)
    short_desc = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    date_published = db.Column(db.String(64), nullable=False)
    publisher = db.Column(db.String(64), nullable=False)
    num_purchased = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        str = "ID: {}    Name: {}    ISBN: {}    Price: {}    Available?: {}    Category_ID: {}    Ratings: {}"
        str = str.format(self.id, self.name, self.isbn, self.price,
                         self.available, self.category_id, self.rating)
        return str


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    date = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)
    books = db.relationship("Book", secondary=orderdetails, backref="orders")

    def __repr__(self):
        str = "ID: {}    Status: {}    First: {}    Surname: {}    Email: {}    Phone: {}    Date: {}    Total Cost: {}    Books in Order: {}"
        str = str.format(self.id, self.status, self.first_name, self.last_name,
                         self.email, self.phone, self.date, self.total_cost, self.book)
        return str
