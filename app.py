from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Customer(db.Model):
    #columns
    accNo=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),nullable=False)
    IDNo=db.Column(db.Integer)
    balance=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    #Function to return acc no as string everytime a new item is created
    def __repr__(self):
        return '<Account number %r>'  %self.accNo

InitialAccNo=0
@app.route('/',methods=['POST','GET'])
def index():
    allCustomers=Customer.query.order_by(Customer.date_created).all()
    return render_template('index.html',allCustomers=allCustomers)

@app.route('/static//register.html',methods=['POST','GET'])
def register():
    if request.method=='POST':
        #customerAccNo=InitialAccNo+1
        customerName=request.form['myName']
        customerIDNo=request.form['IDNo']
        customerInitialDeposit=request.form['balance']

        #new instance of Customer object
        newCustomer=Customer( name=customerName,IDNo=customerIDNo,balance=customerInitialDeposit)

        #push customer to database
        try:
            db.session.add(newCustomer)
            db.session.commit()
            return redirect('/static//login.html') #redirects to login page
        except:
            return "There was an issue adding your details to the database"
    else:
        allCustomers=Customer.query.order_by(Customer.date_created).all()
        return render_template('register.html',allCustomers=allCustomers)

@app.route('/static//login.html',methods=['POST','GET'])
def login():
    allCustomers=Customer.query.order_by(Customer.date_created).all()
    return render_template('login.html',allCustomers=allCustomers)

@app.route('/static/exit.html',methods=['POST','GET'])
def exit():
    allCustomers=Customer.query.order_by(Customer.date_created).all()
    return render_template('exit.html',allCustomers=allCustomers)

if __name__ == "__main__":
    app.run(debug=True)