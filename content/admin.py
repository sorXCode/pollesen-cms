from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from .forms import CKTextAreaField
from .models import Source, Other, Download, Audio, Content
from app import db


def attach_file_field(path="file",**kwargs):
    return form.FileUploadField(base_path=f"static/{path}/",
                                **kwargs,
                                relative_path=path)


class ContentView(ModelView):
    column_editable_list = ['title', ]
    column_searchable_list = ['title', 'subtitle', ]
    column_filters = ['title', 'id', 'subtitle', ]
    # column_list = ["id","title","subtitle","cover_art","script","source","audio","other","download"]
    edit_modal = True
    can_export = True
    page_size = 50
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    can_view_details = True
    column_display_pk = True
    column_hide_backrefs = False

    inline_models = (Source,
                     (Audio, {
                         'form_overrides': {
                             'file': form.FileUploadField
                         },
                         'form_extra_fields': {
                             'file': attach_file_field("other", allowed_extensions=("mp3", "mp4", "m4a", "wav", "wma", "flac", "aac"))
                         }
                     }),
                     (Other, {
                         'form_overrides': {
                             'file': form.FileUploadField
                         },
                         'form_extra_fields': {
                             'file': attach_file_field("other")
                         }
                     }),
                     (Download, {
                         'form_extra_fields': {
                             'file': attach_file_field("download")
                         }
                     }),
                     )
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

    def __init__(self, *args, **kwargs):
        model = Content
        session = db.session
        super().__init__(model, session, *args, **kwargs)
