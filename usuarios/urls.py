from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("CreateNewUser", views.createNewUser),
    path("GetAllUsers", views.getAllUsers),
    path("refresh", views.refresh_token),
]

