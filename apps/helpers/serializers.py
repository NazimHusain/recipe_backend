from rest_framework import serializers
from django.apps import apps
from apps.helpers.models import FileUpload
from typing import Any

DropdownValues = apps.get_model(app_label="helpers", model_name="DropdownValues")


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = FileUpload
        fields = ("id", "file")

    def get_file(self: 'FileUploadSerializer', obj: Any) -> Any:
        try:
            return obj.file.url
        except Exception:
            return None
        
        
class DropDownValueListingSerializer(serializers.Serializer):
    """Serializer of Values Listing."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    display_order = serializers.IntegerField()