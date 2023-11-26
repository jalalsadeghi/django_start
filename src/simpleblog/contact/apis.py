from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema

from simpleblog.contact.models import  Contact
from simpleblog.contact.services import  contact_create


class ContactApi(APIView):

    class InputContactSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=45)
        name = serializers.CharField(max_length=45)
        content = serializers.CharField(max_length=1000)

    class OutPutContactSerializer(serializers.ModelSerializer):

        class Meta:
            model = Contact
            fields = ("email", "name", "content")

    @extend_schema(
        responses=OutPutContactSerializer,
        request=InputContactSerializer,
    )
    def post(self, request):
        serializer = self.InputContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = contact_create(
                email=serializer.validated_data.get("email"),
                name=serializer.validated_data.get("name"),
                content=serializer.validated_data.get("content"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.OutPutContactSerializer(query, context={"request": request}).data)