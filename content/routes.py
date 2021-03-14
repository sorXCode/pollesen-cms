from flask import Blueprint
from flask_restful import Api, Resource, marshal_with
from .models import Content
from app import pagination


content_bp = Blueprint('content_bp', __name__)
api = Api(content_bp)


class AllContents(Resource):
    def get(self):
        return pagination.paginate(Content.query.all(), Content.marshal)


class SingleContent(Resource):
    def get(self, content_id):
        return pagination.paginate(Content.query.filter_by(id=content_id), Content.marshal_detailed)

api.add_resource(AllContents, "/contents")
api.add_resource(SingleContent, "/contents/<int:content_id>")