from django.urls import path
from calculator_app import views

urlpatterns = [
    path("logs/", views.get_calculations, name="get_calculations"),
    path("calc/", views.calculate, name="calculate")
]
