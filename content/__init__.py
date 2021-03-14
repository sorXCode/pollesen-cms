from app import db
from .admin import ContentView
from .models import Content

AdminContentView = ContentView(model=Content, session=db.session)