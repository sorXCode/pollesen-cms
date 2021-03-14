from datetime import datetime
import os


from app import db
from flask_restful import fields
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declared_attr
from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb
import tempfile

class BaseTab(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)

    @declared_attr
    def content_id(cls): return db.Column(
        db.Integer, db.ForeignKey("content.id"))

    marshal = {
        'name': fields.String,
        'link': fields.String,
        'file': fields.String,
    }

    def __repr__(self):
        return "{}: {}".format(self.name, self.link)
    
    def __unicode__(self):
        return self.__repr__()


class Source(BaseTab):
    pass


class Audio(BaseTab):
    pass


class Other(BaseTab):
    pass

class Download(BaseTab):
    pass


class CustomUploadedImageWithThumb(UploadedImageWithThumb):
    def process_content(self, content, filename=None, content_type=None):
        content_location = os.path.join(tempfile.gettempdir(),content)
        
        _content = open(content_location, 'rb')
        super().process_content(content=_content,filename=filename, content_type=content_type)
        
        _content.detach()
        os.remove(content_location)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    cover_art = db.Column(UploadedFileField(
        upload_type=CustomUploadedImageWithThumb))
    created_at = db.Column(db.DateTime, default=datetime.now)
    script = db.Column(db.Text, nullable=False)
    source = db.relationship("Source", backref="content",
                             uselist=True, lazy="dynamic")
    audio = db.relationship("Audio", backref="content",
                            uselist=True, lazy="dynamic")
    other = db.relationship("Other", backref="content",
                            uselist=True, lazy="dynamic")
    download = db.relationship(
        "Download", backref="content", uselist=True, lazy="dynamic")

    @property
    def cover_art_thumbnail(self):
        return self.cover_art.thumb_url
    
    @property
    def cover_art_full(self):
        return self.cover_art.url

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
        'cover_art_full': fields.String,
        'created_at': fields.DateTime,
        'script': fields.String,
        'source': fields.List(fields.Nested(Source.marshal)),
        'other': fields.List(fields.Nested(Other.marshal)),
    }

    def __repr__(self):
        return "<{} {}>".format(self.id, self.title)
