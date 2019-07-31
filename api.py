from flask import Flask
from flask_restful import abort, Api, Resource
from item_model import ArchillectItem
from item_resource import *


app = Flask('__main__')
api = Api(app)


api.add_resource(ArchillectItemResource, '/items/', endpoint='items')


if __name__ == '__main__':
    app.run(debug=True)
