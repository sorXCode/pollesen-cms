from flask import Blueprint
from flask_restful import Api, Resource, marshal_with
from .models import Content


content_bp = Blueprint('content_bp', __name__)
api = Api(content_bp)


class AllContents(Resource):
    @marshal_with(Content.marshal)
    def get(self):
        return Content.query.all()


class SingleContent(Resource):
    @marshal_with(Content.marshal_detailed)
    def get(self, content_id):
        return Content.query.filter_by(id=content_id).first()

api.add_resource(AllContents, "/contents")
api.add_resource(SingleContent, "/contents/<int:content_id>")