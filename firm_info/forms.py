from django import forms

from .compat.editor_widget import TextEditorWidget
from .models import AppsBanner


class AppsBannerForm(forms.ModelForm):
    """
    AppsBanner form.
    """
    class Meta:
        model = AppsBanner
        exclude = []
        fields = [
            "title",
            "application_type",
            "image",
            "description",
        ]
        widgets = {
            "description": TextEditorWidget,
        }
