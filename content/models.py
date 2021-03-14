from datetime import datetime

from app import db
from flask_restful import fields
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_imageattach.entity import Image, image_attachment


class BaseTab(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    file = db.Column(db.String, nullable=False)

    @declared_attr
    def content_id(cls): return db.Column(
        db.Integer, db.ForeignKey("content.id"))

    marshal = {
        'name': fields.String,
        'link': fields.String,
    }

    def __repr__(self):
        return self.name


class Source(BaseTab):
    pass

class Audio(BaseTab):
    pass


class Other(BaseTab):
    pass


class Download(BaseTab):
    pass


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    cover_art = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    script = db.Column(db.Text, nullable=False)
    source = db.relationship("Source", backref="content", uselist=True, lazy="dynamic")
    audio = db.relationship("Audio", backref="content", uselist=True, lazy="dynamic")
    other = db.relationship("Other", backref="content", uselist=True, lazy="dynamic")
    download = db.relationship("Download", backref="content", uselist=True, lazy="dynamic")

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
