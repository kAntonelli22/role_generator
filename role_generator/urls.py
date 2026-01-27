from django.urls import path
from role_generator import views

urlpatterns = [
    path("", views.home, name="home"),
]
