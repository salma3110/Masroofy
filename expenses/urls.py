from django.urls import path
from . import views

urlpatterns = [
    #path('', views.add_expense),  
    path('add/', views.add_expense, name='add'),
    path('history/', views.history, name='history'),
    path('delete/<int:id>/', views.delete_expense, name='delete'),
]