from flask_app.models.user import User
from flask_app.models.order import Order

from flask_app import app

from flask import request, session, render_template, redirect, flash


@app.route('/submit_order',methods=['POST'])
def new_order():
    if 'user_id' not in session:
        flash("You must be signed in to place an order", "register")
        return redirect('/log_reg')
    if not Order.validate_order(request.form):
        print("SOMETHING HERE")
        return redirect('/')
    
    total_scoops = int(request.form["vanilla_scoops"]) + int(request.form["chocolate_scoops"]) + int(request.form["strawberry_scoops"])
    print(total_scoops)
    pretax_amount = round(total_scoops * 3.50, 2)
    print(pretax_amount)
    tax = round(pretax_amount * .08, 2)
    print(tax)
    posttax_amount = round(tax + pretax_amount, 2)
    print(posttax_amount)


    data = {
        "order_amount": posttax_amount,
        "tax" : tax,
        "vanilla_scoops": int(request.form["vanilla_scoops"]),
        "chocolate_scoops": int(request.form["chocolate_scoops"]),
        "strawberry_scoops": int(request.form["strawberry_scoops"]),
        "special_instructions" : request.form["special_instructions"],
        "user_id": session["user_id"]
    }
    print(data)
    Order.save(data)
    return redirect('/success')

@app.route('/update_order',methods=['POST'])
def update_order():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Order.validate_order(request.form):
        print("ERROR")
        
        order_id = request.form["order_id"]
        print(order_id)
        return redirect(f"/edit/{order_id}")
    
    total_scoops = int(request.form["vanilla_scoops"]) + int(request.form["chocolate_scoops"]) + int(request.form["strawberry_scoops"])
    print(total_scoops)
    pretax_amount = round(total_scoops * 3.50, 2)
    print(pretax_amount)
    tax = round(pretax_amount * .08, 2)
    print(tax)
    posttax_amount = round(tax + pretax_amount, 2)
    print(posttax_amount)

    data = {
        "order_amount": posttax_amount,
        "tax" : tax,
        "vanilla_scoops": int(request.form["vanilla_scoops"]),
        "chocolate_scoops": int(request.form["chocolate_scoops"]),
        "strawberry_scoops": int(request.form["strawberry_scoops"]),
        "special_instructions" : request.form["special_instructions"],
        "user_id": session["user_id"],
        "id" : request.form["order_id"]
    }
    print(data)
    
    Order.update(data)
    return redirect('/all_orders')


@app.route('/destroy/<int:id>')
def destroy_order(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Order.destroy(data)
    return redirect('/all_orders')