"""
@file BudgetCycle/urls.py
@brief URL configuration for the BudgetCycle app.

Defines routes for creating and viewing budget cycles.
"""

from django.urls import path
from . import views

app_name = 'budget_cycle'

urlpatterns = [
    path('', views.budget_status, name='budget_home'),   
    path('setup/', views.setup, name='setup'),
    path('change-budget/', views.change_budget, name='change_budget'),
    path('status/', views.budget_status, name='status'),
]
