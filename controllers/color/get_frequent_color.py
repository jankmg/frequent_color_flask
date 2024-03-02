# import flask module
from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from controllers.color.functions.find_frequent_color import find_most_frequent_color

#get frequent color 
class get_frequent_color(Resource):
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
            
            frequent_color = find_most_frequent_color(image_url, 20)
            #if something goes wrong with getting the color, return error response
            if not frequent_color:
                response_data = {"Error": "Something went wrong"}
                return response(409, response_data, mimetype)

            response_data = {"data": {'rgb':frequent_color}}
            return response(200, response_data, mimetype)

        #handle errors            
        except Exception as e:
            return {"messagea": str(e)}, 500
