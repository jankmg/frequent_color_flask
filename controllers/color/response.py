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
