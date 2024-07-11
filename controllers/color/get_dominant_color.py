from flask_restful import Resource, reqparse
from flask import request
from controllers.color.functions.find_frequent_color import find_most_dominant_color
from controllers.color.response import send_response
from controllers.color.response import final_response

class get_dominant_color (Resource):
    def get(self):
        #grab arguments
        args = request.args
        image_url = args["image_url"]
        



        #if user image doesn't exists return error response
        if not image_url:
            return send_response(400, False, "Missing image URL")
        
        frequent_color_data = find_most_dominant_color(image_url, image=False)

        return final_response(frequent_color_data)