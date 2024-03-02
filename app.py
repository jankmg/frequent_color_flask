# import flask module
from flask import Flask
from flask_restful import Api

#import functions
from controllers.color.get_frequent_color import get_frequent_color
from controllers.welcome.welcome import welcome

# instance of flask application
app = Flask(__name__)
api = Api(app)

api.add_resource(welcome, "/")
api.add_resource(get_frequent_color, "/get_most_common_color")

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")