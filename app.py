from flask import Flask
from routes import *
app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(post_routes)
app.register_blueprint(comment_routes)

if __name__ == '__main__':
    app.run()
