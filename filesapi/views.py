from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from drf_social_oauth2.authentication import SocialAuthentication

from .serializers import SharedDataSerializer
from .models import SharedData


class CreateSharedDataInstance(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [OAuth2Authentication, SocialAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SharedDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance_code = serializer.data.get("code")
        instance_url = f"{settings.CLIENT_HOST_URL}/downloads/{instance_code}"

        return Response(
            {"instance": serializer.data, "url": instance_url},
            status=status.HTTP_201_CREATED,
        )


class GetDataInstance(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if code:
            queryset = SharedData.objects.filter(code=code)
            if queryset.exists():
                data_instance = queryset[0]
                serializer = SharedDataSerializer(data_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "invalid code"}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "code not supplied in params"}, status=status.HTTP_400_BAD_REQUEST
        )
