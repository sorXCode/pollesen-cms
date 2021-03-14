from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from .forms import CKTextAreaField
from .models import Source


class ContentView(ModelView):
    inline_models = (Source, )
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'cover_art': form.ImageUploadField,
        'script': CKTextAreaField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_extra_fields = {
        'cover_art': form.ImageUploadField(
                                      base_path="static/",
                                        url_relative_path='',
                                      thumbnail_size=(100, 100, True))
    }


class SourceView(ModelView):
    pass