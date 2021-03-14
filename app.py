import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import config
from flask_pagedown import PageDown
from flask_rest_paginate import Pagination


# load envrionment variables from '.env' file
load_dotenv()


db = SQLAlchemy()
admin = Admin()
pagination = Pagination()


def create_app(environment):
    def init_dependencies(app):
        db.init_app(app)
        admin.init_app(app=app)
        pagination.init_app(app, db)

    def register_blueprints(app):
        from content import AdminContentView, content_bp
        # from flask_admin.contrib.fileadmin.s3 import S3FileAdmin
        
        admin.add_view(AdminContentView)
        app.register_blueprint(content_bp)

        pass

    app = Flask(__name__)
    app.config.from_object(config[environment])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'Slate'
    # app.jinja_env.filters['zip'] = zip

    init_dependencies(app)
    register_blueprints(app)

    return app


# set FLASK_CONFIG to switch environment;
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
