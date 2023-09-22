from waffle_app.config.mysqlconnection import connectToMySQL
from waffle_app import app, DATABASE
from flask import flash
from waffle_app.models.user_model import User

class Waffle:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.comment = data['comment']
        self.img_url = data['img_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = ['user_id']

    @classmethod
    def create(cls, data):

        query ="""
            INSERT INTO waffles (title, comment, img_url, user_id)
            VALUES (%(title)s, %(comment)s, %(img_url)s, %(user_id)s)
        """

        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate(data):
        is_valid = True

        if not data['title']:
            flash('Please enter a title for your post', 'create_err')
            is_valid = False

        if not data['img_url']:
            flash('Please submit an image url', 'create_err')
            is_valid = False

        if not data['comment']:
            flash('Please enter a comment for your post', 'create_err')
            is_valid = False
        elif len(data['comment']) < 5:
            flash('Comment must be longer than 5 characters', 'create_err')
            is_valid = False

        return is_valid
    
    @classmethod
    def get_all_with_users(cls):

        query = """
            SELECT * FROM waffles
            JOIN users ON waffles.user_id = users.id
        """
        results = connectToMySQL(DATABASE).query_db(query)

        waffles = []

        if results:
            for row in results:
                new_waffle = cls(row)

                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }

                new_user = User(user_data)
                new_waffle.user = new_user
                
                waffles.append(new_waffle)

        
        return waffles
    
    @classmethod
    def get_one_with_users(cls, id):

        data = {
            'id' :  id
        }

        query = """
            SELECT * FROM waffles
            JOIN users ON waffles.user_id = users.id
            WHERE waffles.id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        row = results[0]
                
        new_waffle = cls(row)

        user_data = {
            **row,
            'id' : row['users.id'],
            'created_at' : row['users.created_at'],
            'updated_at' : row['users.updated_at']
        }

        new_user = User(user_data)
        new_waffle.user = new_user

        return new_waffle
    
    @classmethod
    def update(cls, data):
        
        query = """
            UPDATE waffles
            SET
                title = %(title)s,
                comment = %(comment)s,
                ing_url = %(img_url)s
            WHERE id = %(id)s
        """

        connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, id):

        data = {
            'id': id
        }

        query = """
            DELETE FROM waffles 
            WHERE id = %(id)s
        """

        connectToMySQL(DATABASE).query_db(query, data)
