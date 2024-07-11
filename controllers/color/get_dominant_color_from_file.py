from flask_restful import Resource, reqparse
import requests
from flask import request
from controllers.color.response import final_response
from controllers.color.functions.find_frequent_color import find_most_dominant_color

class get_dominant_color_from_file (Resource):
    def post(self):
        try:
            #get image from body
            image = request.files.get("image", "")
            print(request.files)
            #if image not exists, raise error
            if not image:
                raise ValueError("Image not provided")
            
            frequent_color_data = find_most_dominant_color(False, image)
        except ValueError as e:
            print("Error: ", )
            return final_response([422, False, str(e), ""])
        except Exception as e:
            print("Error: ", )
            return final_response([422, False, "{message}".format(message=e), ""])
        return final_response(frequent_color_data)
