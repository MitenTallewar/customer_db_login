from flask import Flask,request,render_template,session
from customer_db_login.models import *


@app.route("/createorder", methods=['GET','POST'])
def create_order():
    ord1={'id' : '',
    'orderamount' : ''}
    return render_template("newOrder.html",ord=ord1)


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
    # ord = Orders.query.filter(Customer.id == Orders.id).first()
    print(ord)
    # ord = Orders.query.filter_by(id=oid).first()
    print("=----------------------")
    return render_template('neworder.html',ord = Orders.query.filter_by(id=oid).first())

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
    app.run(debug=True,port=5001)