from app import db
from .views import ContentView, SourceView
from .models import Content, Source

AdminContentView = ContentView(model=Content, session=db.session)
AdminSourceView = SourceView(model=Source, session=db.session)