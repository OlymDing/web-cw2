"""

this python file stores apis that responses to certain requests 

"""

from flaskblog import api
from flask_restful import Resource
from flask import Blueprint

interfaces = Blueprint('interfaces', __name__)

class Test(Resource):
    def get(self):
        return {'wow': 'testing'}

api.add_resource(Test, '/test')
