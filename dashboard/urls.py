"""
@file dashboard/urls.py
@brief URL routes for the dashboard app.

Provides the route for the main dashboard view.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

]
