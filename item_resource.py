from item_model import ArchillectItem
from db import session
from flask_restful import Resource, fields, marshal_with, reqparse
import json

archillect_item_fields = {
    'item_id': fields.Integer,
    'sources': fields.String
}


parser = reqparse.RequestParser()
parser.add_argument('item_id')
parser.add_argument('sources')


class ArchillectItemResource(Resource):
    @marshal_with(archillect_item_fields)
    def get(self):
        items = session.query(ArchillectItem).order_by(ArchillectItem.item_id.desc()).all()
        return items


    @marshal_with(archillect_item_fields)
    def put(self):
        parsed_args = parser.parse_args()
        item = ArchillectItem(
                item_id=parsed_args['item_id'],
                sources_array=json.loads(parsed_args['sources'])
        )
        session.add(item)
        session.commit()
        return item, 201
