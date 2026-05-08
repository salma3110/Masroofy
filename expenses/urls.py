"""
@file expenses/urls.py
@brief URL routes for the expenses app.

Provides routes to add, list, delete and export expense logs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add'),
    path('history/', views.history, name='history'),
    path('delete/<int:id>/', views.delete_expense, name='delete'),
    path('export/', views.export_expenses_csv, name='export'),
]
