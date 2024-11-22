from django.apps import apps
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.helpers import serializers
from apps.helpers import models as HelperModels
from rest_framework.request import Request

DropdownValues = apps.get_model(app_label="helpers", model_name="DropdownValues")
DropdownMaster = apps.get_model(app_label="helpers", model_name="DropdownMaster")


class DropDownMasterListing(APIView):
    serializer_class = serializers.DropDownValueListingSerializer

    def get(self: 'DropDownMasterListing', request: Request, version: str) -> Response:
        queryset = DropdownMaster.objects.filter(is_deleted=False).values(
            "slug", "name"
        )
        return Response(queryset)


class DropDownValuesListingView(APIView):
    serializer_class = serializers.DropDownValueListingSerializer

    def get(
            self: 'DropDownValuesListingView',
            request: Request,
            slug: str,
            version: str
            ) -> Response:
        queryset = DropdownValues.objects.filter(
            dropdownmaster__slug=slug, is_deleted=False
        ).order_by("display_order")
        context = {"request": request}
        serialized = self.serializer_class(queryset, many=True, context=context)
        return Response(serialized.data, 200)


class FileUpload(APIView):
    permission_classes = ()
    def post(self: 'FileUpload', request: Request, version: str) -> Response:
        data = request.data
        createdobj = HelperModels.FileUpload.objects.create(file=data.get("file"))
        return Response(
            {
                "success": True,
                "file": request.build_absolute_uri(createdobj.file.url),
                "id": createdobj.id,
            }
        )