from flask_app.models.user import User
from flask_app.models.order import Order

from flask_app import app

from flask import request, session, render_template, redirect, flash

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/main')

@app.route('/main')
def landing_page():
    if 'user_id' in session:
        user_data = {
            "id":session['user_id']
        }
        user=User.get_by_id(user_data)
        return render_template("landingPage.html", user = user)
    else:
        return render_template("landingPage.html")





#PAGES

@app.route('/log_reg')
def login_register():
    return render_template("log_reg.html")

@app.route('/success')
def success():
    return render_template("order_success.html")


@app.route('/all_orders')
def all_orders():
    data ={
        'id': session['user_id']
    }
    return render_template("my_orders.html", orders=Order.get_all_user_orders(data), user=User.get_by_id(data))


@app.route('/one_order/<int:id>')
def view_one_order(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("one_order.html", order=Order.get_one_user_order(user_data), user=User.get_by_id(user_data))


@app.route("/edit/<int:id>")
def edit_order(id):
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("edit_order.html", order=Order.get_one_user_order(data), user=User.get_by_id(user_data))





#ENTER EXIT APPLICATION
@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/log_reg')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "user_email": request.form['user_email'],
        "user_password": bcrypt.generate_password_hash(request.form['user_password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    
    return redirect("/")


@app.route('/login', methods=["POST"])
def login():
    data = {'user_email' : request.form['user_email'] }

    user_in_db = User.get_by_email(data)


    if not user_in_db:
        flash("EMAIL DOES NOT EXIST", "login")
        print("EMAIL DOES NOT EXIST")
        return redirect("/log_reg")
    
    if not bcrypt.check_password_hash(user_in_db.user_password, request.form['user_password']):
        flash("THE PASSWORDS DID NOT MATCH", "login")
        print("THE PASSWORDS DID NOT MATCH")
        return redirect('/log_reg')


    session['user_id'] = user_in_db.id

    return redirect("/")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




















