from item_model import ArchillectItem
from db import session
from flask_restful import Resource, fields, marshal_with

archillect_item_fields = {
    'item_id': fields.Integer,
    'sources': fields.String
}


class ArchillectItemResource(Resource):
    @marshal_with(archillect_item_fields)
    def get(self):
        items = session.query(ArchillectItem).all()
        return items
