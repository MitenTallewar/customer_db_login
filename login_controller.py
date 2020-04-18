from flask import Flask,request,render_template,session
from models import *

import requests



@app.route("/")
def login():
    # try:
    #     session.pop('utype')
    #     session.pop('msg')
    # except:
    #     pass
    return render_template('login.html')


@app.route("/user/",methods=['GET','POST'])
def authenticate_user():
    userinfo =request.form
    #select * from  user where username= userinfo['username'] and password = userinfo['password'];
    login = user.query.filter(user.username == userinfo['username'],
                              user.password == userinfo['password']).first()
    if login:
        #print(login.id,login.username,login.roleid)
        #select * from role where id = login.roleid;
        role = Role.query.filter(Role.id==login.roleid).first()
       # role = Role.query.filter(user.roleid==login.roleid).first()
       #  print(role.name)
        #select * from customer where id = login.id;
        customer = Customer.query.filter(Customer.id == login.id).first()
        session['username'] = login.username
        session['fname']    = customer.fname
        session['lname']    = customer.lname
        session['role']     = role.name
        if role.name == 'Admin':
            # usertype= 'admin'
            # session['utype'] = usertype
            return render_template("options.html")
            # response = requests.get(BASE_URI+"/customers")
            # # print(response.json())
            #  # return render_template('http://localhost:5000/customers',
            #  #                        msg="Welcome {}".format(login.username)
            #  #                        )
            # return response
        else:
            return render_template("orders.html",
                                   #msg=session['msg'],
                                   orderlist = Orders.query.filter(Orders.cid==customer.id).all()
                                                )

    return render_template("login.html",
                           msg="wrong credential")


@app.route("/logout")
def log_out():
    session['fname']=''
    session['lname']=''
    session['username']=''
    session['role']=''
    return render_template("login.html",
                           msg="You have been logged out successfully...")


@app.route("/customer/register",methods=["GET","POST"])
def save_customer():
    if request.method== 'POST':
    # print(request.form)
        cust = Customer(fname=request.form['fnm'],
                        lname=request.form['lnm'],
                        gender=request.form['gen'],
                        email=request.form['email'],
                        city=request.form['city'],
                        state=request.form['state'],
                        pincode=request.form['pin'],
                        )
        db.session.add(cust)
        role = Role.query.filter(Role.name=="user").first()
        userinfo=user(username=request.form['username'],
                      password=request.form['password'],
                      cust_id=cust.id,
                      roleid=role.id)
        db.session.add(userinfo)
        db.session.commit()
    return render_template("Register.html",
                           customer=Customer,
                           # msg=session['msg'],
                           # msg="customer saved successfully",
                           cust=Customer.dummy_customer())

@app.route("/customers/")
def list_of_customers():
    # if request.method=='GET':
    return render_template("customer.html",
                           # msg=session['msg'],
                           crlist = Customer.query.all())


@app.route("/options")
def admin_options():
    return render_template("options.html")

@app.route("/customer/delete/<int:cid>")
def delete_customer(cid):
    dbcustomer=Customer.query.filter_by(id=cid).first()
    if dbcustomer:
        db.session.delete(dbcustomer)
        db.session.commit()
        username = session['username']
        # userDetails = user.query.filter(user.username == username).first()
        return render_template("customer.html",crlist = Customer.query.all())

@app.route("/createorder", methods=['GET','POST'])
def create_order():
    ord1={'id' : '',
    'orderamount' : ''}
    return render_template("newOrder.html",ord=ord1,pagename="New Order")


@app.route("/order/save",methods=['POST'])
def save_update_orders():
        updateorder=request.form
        username = session['username']
        # print("username from session =",username)
        # select * from user where username = username;
        userDetails = user.query.filter(user.username == username).first()
        # print("update order =",updateorder)
        # print("userdetails =",userDetails)
        if len(updateorder['id']) > 0:
            orderdetails=Orders.query.filter_by(id=updateorder['id']).first()
            print("orderdetails from DB =",orderdetails)
            if orderdetails :
                orderdetails.product = updateorder['product'],
                orderdetails.orderamount = updateorder['amount'],
                orderdetails.cid = userDetails.id
                orderdetails.id = updateorder['id']
                # db.session.add(data)
                # print()
                db.session.commit()

                return render_template("orders.html",
                                       # msg=session['msg'],
                                       # select id orderamount date
                                       # from orders, customer
                                       # where orders.cid = customer.id
                                       # and customer.id = userdetais.id
                                       orderlist=Orders.query.filter(Orders.cid == userDetails.id).all())
            else:
                return render_template('orders.html',orderlist=Orders.query.filter(Orders.cid == userDetails.id).all())
        else:
            ord = Orders(product=request.form['product'],
                         orderamount=request.form['amount'],
                         cid = userDetails.id)
            db.session.add(ord)
            db.session.commit()
            # Fetch orderlist by customer
            # print(orders)
            return render_template("orders.html",
                               # msg=session['msg'],
                               #select id orderamount date
                               # from orders, customer
                               # where orders.cid = customer.id
                               # and customer.id = userdetais.id
                               orderlist = Orders.query.filter(Orders.cid==userDetails.id).all())


@app.route("/orders")
def list_of_orders():
    role = session['role']
    if role ==  "Admin":
        return render_template("orders.html",orderlist=db.session.query(Orders.id,Orders.product, Orders.orderamount, Orders.created_on, Customer.fname).filter(
        Orders.cid == Customer.id))
    else:
        username= session['username']
        userDetails= user.query.filter(user.username==username).first()
        return render_template("orders.html",orderlist=Orders.query.filter(Orders.cid==userDetails.id).all())


@app.route("/orders/edit/<int:oid>")
def fetch_order(oid):
    ord = Orders.query.filter(Customer.id == Orders.id).first()

    print(ord)
    # ord = Orders.query.filter_by(id=oid).first()
    print("=----------------------")
    return render_template('newOrder.html',ord = Orders.query.filter_by(id=oid).first(),pagename="Update your order")


@app.route("/orders/delete/<int:oid>")
def delete_order(oid):
    dborder=Orders.query.filter_by(id=oid).first()
    if dborder:
        db.session.delete(dborder)
        db.session.commit()
        username = session['username']
        userDetails = user.query.filter(user.username == username).first()
        return render_template("orders.html",orderlist=Orders.query.filter(Orders.cid==userDetails.id).all())



if __name__ == '__main__':
    app.run(port=80)