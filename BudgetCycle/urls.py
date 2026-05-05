from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.setup, name='setup'),
    path('change-budget/', views.change_budget, name='change_budget'),
    path('status/', views.budget_status, name='budget_status'),
]