from flask_restful import Resource, reqparse
from controllers.color.functions.find_frequent_color import find_most_dominant_color
from controllers.color.response import send_response

class get_dominant_color (Resource):
    def get(self):
        #grab arguments
        parser = reqparse.RequestParser()
        parser.add_argument("image_url", type=str,  help="URL of th eimage", required=True, location='args')
        arguments = parser.parse_args()
        image_url = arguments["image_url"]



        #if user image doesn't exists return error response
        if not image_url:
            return send_response(400, False, "Missing image URL")
        
        frequent_color_data = find_most_dominant_color(image_url)



        #if something goes wrong with getting the color, return error response
        if not frequent_color_data:
            return send_response(500, False, "Something went wrong")

        if frequent_color_data[0] != 200:
            return send_response(frequent_color_data[0], frequent_color_data[1], frequent_color_data[2], frequent_color_data[3])
        
        hexcolor = "#%02x%02x%02x" % frequent_color_data[3][1]
        #only send data when the request is successfull
        return send_response(200, True, "Most common color successfully found", {"hsl": frequent_color_data[3][0], "rgb": frequent_color_data[3][1], "hex": hexcolor})