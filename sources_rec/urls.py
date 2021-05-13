from django.urls import path
from sources_rec import views

urlpatterns = [
    path("sourcetodb/", views.add_sources, name="add_sources"),
    path("ratingtodb/", views.add_ratings, name="add_ratings"),
]
