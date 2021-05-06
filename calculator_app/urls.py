from django.urls import path
from calculator_app import views

urlpatterns = [
    path("logs/", views.get_calculations, name="get_calculations"),
    path("calc/", views.calculate, name="calculate"),
    path("book/", views.recommend_books, name="recommend_books"),
    path("rec/", views.recommend_sources, name="recommend_sources")
]
