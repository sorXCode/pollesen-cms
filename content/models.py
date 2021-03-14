from app import db
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.event import listens_for
from datetime import datetime
from flask_restful import fields


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))

    marshal = {
        'name': fields.String,
        'link': fields.String,
    }


class Other(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    file = db.Column(db.String, nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))

    marshal = {
        'name': fields.String,
        'file': fields.String,
    }


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    cover_art = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    script = db.Column(db.Text, nullable=False)
    source = db.relationship("Source", backref="content", uselist=True)
    other = db.relationship("Other", backref="content", uselist=True)

    @property
    def cover_art_thumbnail(self):
        splits = self.cover_art.split(".")
        return ".".join(splits[:-1])+"_thumb."+splits[-1]

    marshal = {
        'id': fields.Integer,
        'title': fields.String,
        'subtitle': fields.String,
        'cover_art_thumbnail': fields.String,
        'created_at': fields.DateTime,
    }

    marshal_detailed = {
        'id': fields.Integer,
        'title': fields.String,
        'subtitle': fields.String,
        'cover_art_thumbnail': fields.String,
        'created_at': fields.DateTime,
        "cover_art": fields.String,
        'script': fields.String,
        'source': fields.List(fields.Nested(Source.marshal)),
        'other': fields.List(fields.Nested(Other.marshal)),
    }

    def __repr__(self):
        return "<{} {}>".format(self.id, self.title)


@listens_for(Content, 'after_delete')
def delete_cover_art(mapper, connection, target):
    if target.cover_art:
        try:
            # os.remove(op.join(file_path, target.path))
            pass
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

