from django.urls import path
from sources_rec import views

urlpatterns = [
    path("sourcetodb/", views.add_sources, name="add_sources"),
    path("ratingtodb/", views.add_ratings, name="add_ratings"),
    path("rec/", views.recommend_sources, name="recommend_sources"),
    path("addsource/", views.add_source, name="add_source"),
    path("addrating/", views.add_rating, name="add_rating"),
    path("deleterating/", views.delete_rating, name="delete_rating"),
    path("updaterating/", views.update_rating, name="update_rating"),
]
