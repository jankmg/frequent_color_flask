
# import flask module
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api, reqparse
import json
from types import SimpleNamespace

from PIL import Image
import requests
from io import BytesIO
from collections import Counter

# instance of flask application
app = Flask(__name__)

api = Api(app)
 
class GetData(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image_url", type=str,  help="URL of th eimage", required=True, location='args')
        arguments = parser.parse_args()
        image_url = arguments["image_url"]
        

        def get_pixels_from_image(url):
            #get and open image from url
            img = requests.get(url) 
            image = Image.open(BytesIO(img.content))

            #get the pixels from the image
            pixels = image.getdata()
            return pixels


        def get_top_frequent_colors(pixels, length):
            count = Counter(pixels)
            frequent_colors = count.most_common(length)
            return frequent_colors


        def get_frequent_color(most_frequent_colors, offset):
            #if the most frequent color is darker set value or lighter than set value save it as frequent color
            most_frequent = (0,0,0)
            for freq in most_frequent_colors:
                frequent = tuple(sorted(freq[0], reverse=True))
                if frequent[0] - frequent[1] < offset and frequent[1] - frequent[2] < offset:
                    continue
                else:
                    most_frequent = freq[0]
            return most_frequent

        def print_most_frequent_color(url, offset):
            pixels = get_pixels_from_image(url)
            top_frequent_colors = get_top_frequent_colors(pixels, len(pixels))
            frequent_color = get_frequent_color(top_frequent_colors, offset)
            return frequent_color
        

        def response(status, data, type):
            response = make_response(jsonify(data))
            response.headers["customHeader"] = "this is a custom header"
            response.status_code = status
            response.mimetype = type

            return response

        try:
            mimetype = 'application/json'
            if not image_url:
                response_data = {"error": "Missing image url"}
                return response(400, response_data, mimetype)
            
            frequent_color = print_most_frequent_color(image_url, 20)
            if not frequent_color:
                response_data = {"Error": "Something went wrong"}
                return response(409, response_data, mimetype)

            response_data = {"data": {'rgb':frequent_color}}
            return response(200, response_data, mimetype)
            
        except Exception as e:
            return {"messagea": str(e)}, 500



api.add_resource(GetData, "/get_most_common_color")

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")