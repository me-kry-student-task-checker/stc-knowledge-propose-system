from django.urls import path
from calculator_app import views

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
]