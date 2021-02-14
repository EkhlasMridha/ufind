from django.urls import path, include
from ufindAPI.identityapi import (
    login_api_view,
    register_api_view,
    get_profile_api
)

from ufindAPI.missingpersonapi import (
    submit_case_view
)

urlpatterns = [
    path('login', login_api_view, name="login"),
    path('register', register_api_view, name='register'),
    path('profile', get_profile_api, name="profile"),
    path('case', submit_case_view, name="case")
]
