from django.urls import include, path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('setup/', views.setup, name='setup'),
    path('login/', views.login, name='login'),
    path('lockout/', views.lockout, name='lockout'),
]