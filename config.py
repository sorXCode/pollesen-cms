import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_REFRESH_EACH_REQUEST = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'development_db.sqlite')
    # Flask-User settings
    USER_APP_NAME = "CMS"      # Shown in and email templates and page footers
    USE_S3 = True
    S3_BUCKET_NAME = "6d5c3e43b8fb4fd8ac6c72ea99925ff5"
    S3_REGION = os.environ["S3_REGION"]
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024



config = {
    'development': Config,
    'default': Config
}
