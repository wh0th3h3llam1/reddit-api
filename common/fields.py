from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SlugCreateOnlyField(serializers.CreateOnlyDefault):
    def __init__(self, default) -> None:
        super().__init__(default)


class RichTextEditorSerializerField(serializers.CharField):
    default_error_messages = {"invalid": _("Enter valid text.")}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        str_value = super().to_internal_value(data)
        # text = to_python(str_value, region=self.region)

        # if text and not text.is_valid():
        #     raise ValidationError(self.error_messages["invalid"])
        return str_value
