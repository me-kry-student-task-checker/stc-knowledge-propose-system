from django.urls import path
from sources_rec import views

urlpatterns = [
    path("model/rec/", views.recommend_sources, name="recommend_sources"),
    path("model/build/", views.build_recommender_model, name="build_recommender_model"),
    path("source/add/", views.add_source, name="add_source"),
    path("source/get/", views.get_sources, name="get_sources"),
    path("source/findby-id/", views.get_source, name="get_source"),
    path("source/delete/", views.delete_source, name="delete_source"),
    path("source/update/", views.update_source, name="update_source"),
    path("rating/add/", views.add_rating, name="add_rating"),
    path("rating/findby-user/", views.get_user_ratings, name="get_user_ratings"),
    path("rating/findby-source/", views.get_source_ratings, name="get_source_ratings"),
    path("rating/findby-source-user/", views.get_source_and_user_ratings, name="get_source_and_user_ratings"),
    path("rating/delete/", views.delete_rating, name="delete_rating"),
    path("rating/update/", views.update_rating, name="update_rating"),
]
