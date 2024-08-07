# import flask module
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

#import functions
from controllers.color.get_dominant_color import get_dominant_color
from controllers.color.get_dominant_color_from_file import get_dominant_color_from_file
from controllers.welcome.welcome import welcome

# instance of flask application
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(welcome, "/")
api.add_resource(get_dominant_color, "/get_dominant_color")
api.add_resource(get_dominant_color_from_file, "/get_dominant_color_from_file")

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")