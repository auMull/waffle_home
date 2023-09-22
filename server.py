from waffle_app import app
from waffle_app.controllers import user_controller
from waffle_app.controllers import waffle_controller

if __name__ == "__main__":
    app.run(debug=True)