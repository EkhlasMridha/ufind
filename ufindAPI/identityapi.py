import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail

from user.serializers import UserRegistrationSerializer, UserProfileSerializer, ChangePasswordSerializer
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


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_request_view(request):
    useremail = request.data['email']

    if useremail is None:
        return Response({'message': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    userCount = User.objects.filter(email=useremail).count()
    if userCount == 0:
        return Response({'message': 'No user with this email'}, status=status.HTTP_200_OK)
    user = User.objects.get(email=useremail)
    reset_token = jwt.encode({'mail': useremail}, user.password)
    mailBody = "Click on the link to reset your password: http://localhost:4200/reset?token=" + reset_token
    send_mail(
        "Reset request",
        mailBody,
        "vootwap@gmail.com",
        [useremail],
        fail_silently=False
    )

    return Response({'message': "Mail sent with reset request"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_view(request):
    reset_payload = request.data
    user = User.objects.get(email=reset_payload.email)
    decoded = jwt.decode(reset_payload.token,
                         user.password, algorithms='HS256')
    user.set_password(reset_payload.password)
    user.save()

    return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = auth.authenticate(email=email, password=password)

    if (user is None):
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    auth_token = jwt.encode(
        {'id': user.id, 'email': user.email, 'isAdmin': user.is_superuser}, settings.JWT_SECRET)

    data = {'token': auth_token, 'isAdmin': user.is_superuser}

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_api(request):
    user = request.user
    s_user = UserProfileSerializer(user).data

    return Response(s_user, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, HasAdminPermission])
def get_userlist_view(request):
    mail = request.user.email
    userlist = User.objects.exclude(email=mail)
    serialized = UserProfileSerializer(userlist, many=True)

    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    email = request.user.email
    password = request.data.get('oldpass')

    authUser = auth.authenticate(email=email, password=password)

    if (authUser is None):
        return Response({'message': 'Invalid credential'}, status=status.HTTP_400_BAD_REQUEST)

    authUser.set_password(request.data.get('newpass'))
    authUser.save()

    return Response({"meesage": 'password changed successfully'}, status=status.HTTP_200_OK)
