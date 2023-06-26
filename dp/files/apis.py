from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dp.api.mixins import ApiAuthMixin
from dp.files.models import File
from dp.files.services import (
    FileDirectUploadService,
    FileStandardUploadService,
)

from drf_spectacular.utils import extend_schema


class FileStandardUploadApi(ApiAuthMixin, APIView):
    
    @extend_schema(request=None, responses=None)
    def post(self, request):
        service = FileStandardUploadService(user=request.user, file_obj=request.FILES["file"])
        file = service.create()

        return Response(data={"id": file.id}, status=status.HTTP_201_CREATED)


class FileDirectUploadStartApi(ApiAuthMixin, APIView):
    class InputDirectUploadStartSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    @extend_schema(
            request=InputDirectUploadStartSerializer,
            responses=None
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputDirectUploadStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = FileDirectUploadService(request.user)
        presigned_data = service.start(**serializer.validated_data)

        return Response(data=presigned_data)


class FileDirectUploadLocalApi(ApiAuthMixin, APIView):

    @extend_schema(request=None, responses=None)
    def post(self, request, file_id):
        file = get_object_or_404(File, id=file_id)

        file_obj = request.FILES["file"]

        service = FileDirectUploadService(request.user)
        file = service.upload_local(file=file, file_obj=file_obj)
        
        return Response({"id": file.id})


class FileDirectUploadFinishApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField()

    @extend_schema(request=None, responses=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_id = serializer.validated_data["file_id"]

        file = get_object_or_404(File, id=file_id)

        service = FileDirectUploadService(request.user)
        service.finish(file=file)

        return Response({"id": file.id})
