# import flask module
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import awsgi

#import functions
from controllers.color.get_dominant_color import get_dominant_color
from controllers.welcome.welcome import welcome

# instance of flask application
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(welcome, "/")
api.add_resource(get_dominant_color, "/get_dominant_color")


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

# if __name__ == '__main__':
#     app.run(debug=True, port=8080, host="0.0.0.0")