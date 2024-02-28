
# import flask module
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api, reqparse

from PIL import Image
import requests
from io import BytesIO
from collections import Counter

from get_frequent_color import get_most_frequent_color

# instance of flask application
app = Flask(__name__)
api = Api(app)

#Welcom page
class Welcome(Resource):
    def get(self):
        return {"Message": "Hello world"}

#get frequent color 
class GetData(Resource):
    def get(self):
        #grab arguments
        parser = reqparse.RequestParser()
        parser.add_argument("image_url", type=str,  help="URL of th eimage", required=True, location='args')
        arguments = parser.parse_args()
        image_url = arguments["image_url"]

        #response constructor
        def response(status, data, type):
            response = make_response(jsonify(data))
            response.headers["customHeader"] = "this is a custom header"
            response.status_code = status
            response.mimetype = type
            return response

        try:
            mimetype = 'application/json'
            #if user image doesn't exists return error response
            if not image_url:
                response_data = {"error": "Missing image url"}
                return response(400, response_data, mimetype)
            
            frequent_color = get_most_frequent_color(image_url, 20)
            #if something goes wrong with getting the color, return error response
            if not frequent_color:
                response_data = {"Error": "Something went wrong"}
                return response(409, response_data, mimetype)

            response_data = {"data": {'rgb':frequent_color}}
            return response(200, response_data, mimetype)

        #handle errors            
        except Exception as e:
            return {"messagea": str(e)}, 500



api.add_resource(Welcome, "/")
api.add_resource(GetData, "/get_most_common_color")

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")