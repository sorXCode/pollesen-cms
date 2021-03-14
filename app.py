
from dotenv import load_dotenv
# load envrionment variables from '.env' file
load_dotenv()


from dep import storage
from depot.manager import DepotManager
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin, S3Storage
from flask_rest_paginate import Pagination
from flask_pagedown import PageDown
from config import config, Config
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, session
import os
from datetime import timedelta


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

        admin.add_view(AdminContentView)
        admin.add_view(S3FileAdmin(bucket_name=Config.S3_BUCKET_NAME, region=Config.S3_REGION,
                                   aws_access_key_id=Config.AWS_ACCESS_KEY_ID, aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY))
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
