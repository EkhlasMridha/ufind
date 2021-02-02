from django.urls import path, include
from ufindAPI.authapi import (
    login_api_view,
    register_api_view
)

urlpatterns = [
    path('login', login_api_view, name="login"),
    path('register', register_api_view, name='register')
]
