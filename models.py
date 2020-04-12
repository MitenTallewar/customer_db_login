from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/loginapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = '218AHDJAHD3243284787ADSJ'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column('id',db.Integer(),primary_key=True)
    fname = db.Column('first_name',db.String(50))
    lname = db.Column('last_name',db.String(50))
    gender = db.Column('gender', db.String(50))
    email = db.Column('email',db.String(50))
    city = db.Column('city', db.String(50))
    state = db.Column('state', db.String(50))
    pincode = db.Column('pincode', db.Integer())
    order=db.relationship('Orders',cascade="all,delete",backref='Customer')
    userref= db.relationship('user',cascade="all,delete",backref='Customer')

    @staticmethod
    def dummy_customer():
        return Customer(id=0, fname='', lname='', gender='',email='', city='', state='', pincode='')


class user(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    username = db.Column('username', db.String(50))
    password = db.Column('password', db.String(50))
    roleid = db.Column("role_id", db.ForeignKey('role.id'), unique=False)
    cust_id= db.Column("customer_id",db.ForeignKey('customer.id'),unique=True)

class Role(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(50))


class Orders(db.Model):
    id = db.Column('or_id', db.Integer(), primary_key=True)
    product = db.Column('product',db.String(50))
    orderamount = db.Column('amount', db.Float())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    cid = db.Column("cust_id",db.ForeignKey('customer.id'),unique=False,nullable=False)

if __name__ == '__main__':
    # c1 = Customer(id=2,fname="Jay",lname="Mule",gender ="Male",email="jay@gmail.com",city="ahmedabad",state="Gujrat",pincode =395089)
    # c2 = Customer(id=3, fname="pranav", lname="Tallewar", gender="Male", email="jay@gmail.com", city="ahmedabad",state="Gujrat", pincode=395089)
    # c3 = Customer(id=4, fname="Pooja", lname="Mule", gender="Female", email="jay@gmail.com", city="ahmedabad",state="Gujrat", pincode=395089)
    # db.session.add_all([c1,c2,c3])
    # db.session.commit()
    #  db.drop_all()
    # d1= Orders(orderamount=100,cid=1)
    # db.session.add(d1)
    # db.session.commit()
    #  Orders.__table__.create(session.bind)
    # query = db.session.query(Orders.id, Orders.orderamount, Orders.created_on, Customer.fname).filter(
    #     Orders.cid == Customer.id)
    # # print(query)
    # for obj in query:
    #     print(obj)
    #
    # ord = Orders.query.filter(Customer.id==Orders.id).first()
    # print(ord)
     db.create_all()