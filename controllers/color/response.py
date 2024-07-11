from flask import jsonify, make_response

def send_response(status, success, message, data):
    mimetype = 'application/json'
    
    response_data = {"status": status, "success": success, "message": message}

    if status == 200:
        response_data = {"status": status, "success": success, "message": message, "data": data}

    return response(status, response_data, mimetype)

#response constructor
def response(status, data, type):
    response = make_response(jsonify(data))
    response.headers["customHeader"] = "this is a custom header"
    response.status_code = status
    response.mimetype = type
    return response

def final_response(frequent_color_data):
    print(frequent_color_data)
    #if something goes wrong with getting the color, return error response
    if not frequent_color_data:
        return send_response(500, False, "Something went wrong")

    if frequent_color_data[0] != 200:
        return send_response(frequent_color_data[0], frequent_color_data[1], frequent_color_data[2], frequent_color_data[3])
    
    hexcolor = "#%02x%02x%02x" % frequent_color_data[3][1]
    #only send data when the request is successfull
    return send_response(200, True, "Most common color successfully found", {"hsl": frequent_color_data[3][0], "rgb": frequent_color_data[3][1], "hex": hexcolor})