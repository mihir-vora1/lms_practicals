from django import forms
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget

class CKEditorUserModuleWidget(CKEditorWidget):
    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        return mark_safe(f'{rendered}<script type="text/javascript">CKEDITOR.replace("{name}", {{ customConfig: "/static/js/ckeditor-config.js" }});</script>')