from django.urls import include, path
"""
@file authentication/urls.py
@brief URL routes for the authentication app.

Defines named routes for setup, login and lockout views.
"""

from . import views

app_name = 'authentication'

urlpatterns = [
    path('setup/', views.setup, name='setup'),
    path('login/', views.login, name='login'),
    path('lockout/', views.lockout, name='lockout'),
]
