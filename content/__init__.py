from app import db
from .views import ContentView
from .models import Content

AdminContentView = ContentView(model=Content, session=db.session)