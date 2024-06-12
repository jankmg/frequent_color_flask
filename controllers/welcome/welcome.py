from flask_restful import Resource

#Welcom page
class welcome(Resource):
    def get(self):
        return {"Message": "Hello world", "version": "2.0"}