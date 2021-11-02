from django.urls import path
from sources_rec import views

urlpatterns = [
    path("sourcetodb/", views.add_sources, name="add_sources"),
    path("ratingtodb/", views.add_ratings, name="add_ratings"),
    path("rec/", views.recommend_sources, name="recommend_sources"),
    path("buildmodel/", views.build_recommender_model, name="build_recommender_model"),
    path("addsource/", views.add_source, name="add_source"),
    path("getsources/", views.get_sources, name="get_sources"),
    path("getsource/", views.get_source, name="get_source"),
    path("deletesource/", views.delete_source, name="delete_source"),
    path("updatesource/", views.update_source, name="update_source"),
    path("addrating/", views.add_rating, name="add_rating"),
    path("getuserratings/", views.get_user_ratings, name="get_user_ratings"),
    path("getsourceratings/", views.get_source_ratings, name="get_source_ratings"),
    path("getsourceanduserratings/", views.get_source_and_user_ratings, name="get_source_and_user_ratings"),
    path("deleterating/", views.delete_rating, name="delete_rating"),
    path("updaterating/", views.update_rating, name="update_rating"),
]
