from app import db
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.event import listens_for
from datetime import datetime


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    subtitle = db.Column(db.String(), nullable=False)
    cover_art = db.Column(db.String())
    script = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    source = db.relationship("Source", backref="content", uselist=True)


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


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    # content = db.relationship("Content", back_populates="source")

