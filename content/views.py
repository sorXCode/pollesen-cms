from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from .forms import CKTextAreaField
from .models import Source, Other


class ContentView(ModelView):
    inline_models = (Source,
                     (Other, {
                         'form_overrides': {
                             'file': form.FileUploadField
                         },
                         'form_extra_fields': {
                             'file': form.FileUploadField(
                                 base_path="static/other/",
                                 relative_path='other')
                         }
                     }),)
    column_editable_list = ['title', ]
    can_export = True

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'cover_art': form.ImageUploadField,
        'script': CKTextAreaField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_extra_fields = {
        'cover_art': form.ImageUploadField(
            base_path="static/cover_art/",
            url_relative_path='cover_art/',
            thumbnail_size=(200, 200, True))
    }


class SourceView(ModelView):
    pass
