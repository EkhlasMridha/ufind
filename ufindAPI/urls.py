from django.urls import path, include
from ufindAPI.identityapi import (
    login_api_view,
    register_api_view,
    get_profile_api,
    get_userlist_view,
    reset_request_view,
    change_password
)

from ufindAPI.missingpersonapi import (
    submit_case_view,
    get_cases_view,
    case_data_found,
    get_all_cases,
    match_person_view,
    delete_case_view,
    mark_as_solved
)

urlpatterns = [
    path('login', login_api_view, name="login"),
    path('register', register_api_view, name='register'),
    path('profile', get_profile_api, name="profile"),
    path('case', submit_case_view, name="case"),
    path('get-cases', get_cases_view, name='get-cases'),
    path('found', case_data_found, name="found"),
    path('allcase', get_all_cases, name="allcase"),
    path('alluser', get_userlist_view, name='alluser'),
    path('match', match_person_view, name="match"),
    path('reset-password', reset_request_view, name='reset-password'),
    path('change-password', change_password, name='change-password'),
    path('delete-case', delete_case_view, name='delete-case'),
    path('make-solved', mark_as_solved, name='make-solved')
]
