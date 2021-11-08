from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from sources_rec import service
from sources_rec import models
from sources_rec import validators
from sources_rec import model_builder


@api_view(["POST"])
def add_sources(request):
    service.sources_to_db()
    return Response()


@api_view(["POST"])
def add_ratings(request):
    service.ratings_to_db()
    return Response()


@api_view(["POST"])
def recommend_sources(request):
    user_id = request.data.get("userid")
    try:
        result = service.recommend_sources(user_id)
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(result)


@api_view(["PUT"])
def build_recommender_model(request):
    model_builder.build_recommender_model()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def add_source(request):
    source = {
        "title": request.data.get("title"),
        "topic": request.data.get("topic"),
        "url": request.data.get("url"),
        "average_rating": 0,
        "ratings_count": 0,
        "ratings_1": 0,
        "ratings_2": 0,
        "ratings_3": 0,
        "ratings_4": 0,
        "ratings_5": 0
    }
    try:
        validators.validate_source_input(source)
        service.add_source(source)
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_sources(request):
    sources = service.get_sources()
    return Response(sources)


@api_view(["POST"])
def get_source(request):
    source_id = request.data.get("source")
    try:
        validators.validate_get_source_input(source_id)
        source = service.get_source(source_id)
    except (ValidationError, models.Source.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(source)


@api_view(["DELETE"])
def delete_source(request):
    source_id = request.data.get("source")
    try:
        validators.validate_delete_source_input(source_id)
        service.delete_source(source_id)
    except (ValidationError, models.Source.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_source(request):
    source = {
        "source_id": request.data.get("source_id"),
        "title": request.data.get("title"),
        "topic": request.data.get("topic"),
        "url": request.data.get("url"),
    }
    try:
        validators.validate_delete_source_input(source["source_id"])
        validators.validate_source_input(source)
        service.update_source(source)
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def add_rating(request):
    rating = {
        "source": request.data.get("source"),
        "user": request.data.get("user"),
        "rating": request.data.get("rating"),
    }
    try:
        validators.validate_rating_input(rating)
        service.add_rating(rating)
    except (ValidationError, models.Source.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def get_user_ratings(request):
    user = request.data.get("user")
    try:
        validators.validate_user_ratings_input(user)
        ratings = service.get_user_ratings(user)
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(ratings)


@api_view(["POST"])
def get_source_ratings(request):
    source = request.data.get("source")
    try:
        validators.validate_user_ratings_input(source)
        ratings = service.get_source_ratings(source)
    except ValidationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(ratings)


@api_view(["POST"])
def get_source_and_user_ratings(request):
    source = request.data.get("source")
    user = request.data.get("user")
    try:
        validators.validate_user_ratings_input(source)
        validators.validate_user_ratings_input(user)
        ratings = service.get_source_and_user_ratings(source, user)
    except (ValidationError, models.Rating.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(ratings)


@api_view(["DELETE"])
def delete_rating(request):
    rating = {
        "source": request.data.get("source"),
        "user": request.data.get("user"),
    }
    try:
        validators.validate_delete_rating_input(rating)
        service.delete_rating(rating)
    except (ValidationError, models.Rating.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_rating(request):
    rating = {
        "source": request.data.get("source"),
        "user": request.data.get("user"),
        "rating": request.data.get("rating"),
    }
    try:
        validators.validate_rating_input(rating)
        service.update_rating(rating)
    except (ValidationError, models.Rating.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)
