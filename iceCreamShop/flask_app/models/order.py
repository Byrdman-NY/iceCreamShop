from flask_app.config.mySQLConnection import connectToMySQL
from flask_app import app
import re
from flask import flash
from pprint import pprint

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

db = "storeDB"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class Order:
    def __init__(self, data):
        self.id = data['id']
        self.order_amount = data['order_amount']
        self.tax = data["tax"]
        self.user_id = data['user_id']
        self.vanilla_scoops = data['vanilla_scoops']
        self.chocolate_scoops = data['chocolate_scoops']
        self.strawberry_scoops = data['strawberry_scoops']
        self.special_instructions = data['special_instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_order(order):
        is_valid = True
        total_scoops = int(order["vanilla_scoops"]) + int(order["chocolate_scoops"]) + int(order["strawberry_scoops"])
        print(total_scoops)
        if int(total_scoops) < 4:
            flash("Please select at least 4 scoops total", "order")
            is_valid = False
        if len(order['special_instructions']) < 10:
            flash("Please leave a description of how you want your order made (Minimum 10 characters)", "order")
            is_valid= False
        return is_valid
        

    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders (order_amount, tax, user_id, vanilla_scoops, chocolate_scoops, strawberry_scoops, special_instructions) VALUES (%(order_amount)s, %(tax)s, %(user_id)s,%(vanilla_scoops)s,%(chocolate_scoops)s,%(strawberry_scoops)s, %(special_instructions)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_all_user_orders(cls, data):
        query  = "SELECT * FROM orders WHERE user_id = %(id)s";
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def get_one_user_order(cls, data):
        query  = "SELECT * FROM orders WHERE id = %(id)s";
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE orders SET order_amount=%(order_amount)s, tax=%(tax)s, user_id=%(user_id)s, vanilla_scoops=%(vanilla_scoops)s, chocolate_scoops=%(chocolate_scoops)s, strawberry_scoops=%(strawberry_scoops)s, special_instructions=%(special_instructions)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    


    @classmethod
    def destroy(cls, data):
        query  = "DELETE FROM orders WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    