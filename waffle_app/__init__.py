from flask import Flask
app = Flask(__name__)

app.secret_key = 'secret'

DATABASE = 'waffle_db'