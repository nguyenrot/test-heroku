from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer, EmailVerificationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import User
from .utils import Util
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes, api_view
import jwt, requests
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class AuthInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        r = requests.post(
            'http://127.0.0.1:8000/auth/o/token/',
            data={
                'grant_type': 'password',
                'username': request.data.get('username'),
                'password': request.data.get('password'),
                'client_id': settings.OAUTH2_INFO["CLIENT_ID"],
                'client_secret': settings.OAUTH2_INFO["CLIENT_SECRET"],
            },
        )
        return Response(r.json())


class UserViewSet(generics.GenericAPIView):
    serializer_class = UserSerializer

    # renderer_classes = (UserRender,)
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm='HS256')

        current_site = get_current_site(request).domain

        relative_link = reverse('verify-email')

        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username + 'Use link below to verify your email \n' + abs_url
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_403_FORBIDDEN)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
