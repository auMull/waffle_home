from waffle_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
from waffle_app import app, DATABASE
import re

bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    @classmethod
    def register_user(cls, data):
    
        query ="""
            INSERT INTO users (username, first_name, email, password)
            VALUES (%(username)s, %(first_name)s, %(email)s, %(password)s)
        """

        hashed_pass = bcrypt.generate_password_hash(data['password'])

        user_data = {
            **data,
            'password' : hashed_pass
        }


        connectToMySQL(DATABASE).query_db(query, user_data)


    @classmethod
    def get_one_by_username(cls, username):
        data ={
            'username' :  username
        }

        query = """
            SELECT * FROM users WHERE username = %(username)s;
        """

        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if results:
            result = results[0]
            return cls(result)
        else:
            return False
    
    @classmethod
    def login_user(cls, data):
        found_user = cls.get_one_by_username(data['username'])

        if found_user:

            if bcrypt.check_password_hash(found_user.password, data['password']):
                return found_user
         
            else:
                flash('Invalid login', 'login')
                return False
            
        else:
            flash('Invalid login', 'login')
            return False


    @classmethod
    def validate(cls, form):
        is_valid = True

        if len(form['username']) < 1:
            flash("Must enter a desired username", 'signup')
            is_valid = False

        #first name length
        if len(form['first_name']) < 2:
            flash("First name too short", 'signup')
            is_valid = False



        #checks if username and email is already in the database
        if User.get_one_by_username (form['username']):
            flash("Username already exists", 'signup')
            is_valid = False


        #checks if the email is in proper email format
        if bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', form['email'])) == False:
            flash("Email is invalid", 'signup')
            is_valid = False




        #checks if the password is long enough
        if len(form['password']) < 8:
            flash("Password must be at least 8 characters", 'signup')
            is_valid = False

        #checks if the password and the confirm password are the same
        if form['password'] != form['confirm_password']:
            flash("Passwords do not match", 'signup')
            is_valid = False


        return is_valid