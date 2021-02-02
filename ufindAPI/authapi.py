import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings
from django.contrib import auth

from user.serializers import UserRegistrationSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api_view(request):
    serialized = UserRegistrationSerializer(request.data)
    responseData = {}

    if serialized.is_valid():
        user = serialized.save()
        responseData['email'] = user.email
        responseData['name'] = user.name
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
