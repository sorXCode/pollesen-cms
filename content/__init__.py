from app import db
from .admin import ContentView
from .models import Content
from .routes import content_bp

AdminContentView = ContentView(model=Content, session=db.session)