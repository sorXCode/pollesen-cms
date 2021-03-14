from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from .forms import CKTextAreaField
from .models import Source, Other, Download, Audio, Content
from app import db, storage
import tempfile

def attach_file_field(path="file", **kwargs):
    return form.FileUploadField(base_path=f"static/{path}/",
                                **kwargs,
                                relative_path=path)

def enumerate_objects(objects):
    return ["{}: {}\n".format(x, obj) for x, obj in enumerate(objects, start=1)]

class ContentView(ModelView):
    column_editable_list = ['title', ]
    column_searchable_list = ['title', 'subtitle', ]
    column_filters = ['title', 'id', 'subtitle', ]
    column_list = ["id","title","subtitle","cover_art","script","source","audio","other","download"]
    # edit_modal = True
    can_export = True
    page_size = 50
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    can_view_details = True
    column_display_pk = True
    column_hide_backrefs = False
    column_formatters = {
        "cover_art": lambda v, context, model, name: model.cover_art.url,
        "source": lambda v, context, model, name: enumerate_objects(model.source.all()),
        "audio": lambda v, context, model, name: enumerate_objects(model.audio.all()),
        "other": lambda v, context, model, name: enumerate_objects(model.other.all()),
        "download": lambda v, context, model, name: enumerate_objects(model.download.all()),
    }

    inline_models = (Source,
                     Audio,
                     Other,
                     Download,
                     )
    column_editable_list = ['title', ]
    can_export = True

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'cover_art': form.FileUploadField,
        'script': CKTextAreaField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_extra_fields = {
        'cover_art': form.FileUploadField(
            base_path=tempfile.gettempdir()
            )
    }

    def __init__(self, *args, **kwargs):
        model = Content
        session = db.session
        super().__init__(model, session, *args, **kwargs)
