from app import db
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.event import listens_for


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    cover_art = db.Column(db.String())

@listens_for(Content, 'after_delete')
def delete_cover_art(mapper, connection, target):
    if target.cover_art:
        try:
            # os.remove(op.join(file_path, target.path))
            pass
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass