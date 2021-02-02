import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail

from user.serializers import UserRegistrationSerializer, UserProfileSerializer
from user.models import User
from ufindAPI.ufindpermissions import HasAdminPermission
from user.passgenerator import generate_password

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasAdminPermission])
def register_api_view(request):
    request.data['password'] = generate_password(8)
    serialized = UserRegistrationSerializer(data=request.data)
    mailBody = "Your account credentials: email: "+request.data['email']+" password: " + \
        request.data['password'] + \
        ". Please change your credential after loging in"
    responseData = {}

    if serialized.is_valid():
        user = serialized.save()
        responseData['email'] = user.email
        responseData['name'] = user.name

        send_mail(
            "Welcome to U-Finder",
            mailBody,
            "vootwap@gmail.com",
            [user.email],
            fail_silently=False
        )
    else:
        responseData['message'] = serialized.errors

    return Response(data=responseData)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = auth.authenticate(email=email, password=password)

    if (user is None):
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    auth_token = jwt.encode(
        {'email': user.email, 'isAdmin': user.is_superuser}, settings.JWT_SECRET)

    data = {'token': auth_token}

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_api(request):
    user = request.user
    s_user = UserProfileSerializer(user).data

    return Response(s_user, status=status.HTTP_200_OK)
