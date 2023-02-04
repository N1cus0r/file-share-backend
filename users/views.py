from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from drf_social_oauth2.authentication import SocialAuthentication

from .serializers import (
    CreateCustomUserSerializer,
    CustomUserSerializer,
    PasswordResetEmailSerializer,
    PerformPasswordResetSerializer,
    ActivateAccountSerializer,
    EditProfileSerializer,
)
from .models import CustomUser
from .utils import Util


class CreateUser(APIView):
    serializer_class = CreateCustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivateUserAccount(APIView):
    serializer_class = ActivateAccountSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Account activated"}, status=status.HTTP_200_OK)


class GetUserInfo(APIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [OAuth2Authentication, SocialAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")
        if email:
            queryset = CustomUser.objects.filter(email=email)
            if queryset.exists():
                user = queryset[0]
                if user.is_active:
                    serializer = self.serializer_class(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "inactive account"})
            return Response(
                {"error": "invalid email"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"error": "email was not found in params"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetPasswordResetEmail(APIView):
    serializer_class = PasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "We have sent you an email"}, status=status.HTTP_200_OK
        )


class PerformPasswordReset(APIView):
    serializer_class = PerformPasswordResetSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset successfully"}, status=status.HTTP_200_OK
        )


class GetEditProfileUID(APIView):
    authentication_classes = [OAuth2Authentication, SocialAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")
        if email:
            queryset = CustomUser.objects.filter(email=email)
            if queryset.exists():
                user = queryset[0]
                encoded_id = Util.get_encoded_user_id(user)
                return Response(encoded_id, status=status.HTTP_200_OK)
            return Response(
                {"error": "Invalid email"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"error": "Email was not provided in params "},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EditProfile(APIView):
    serializer_class = EditProfileSerializer
    authentication_classes = [OAuth2Authentication, SocialAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
