from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from sources_rec import service


@api_view(["POST"])
def add_sources(request):
    service.sources_to_db()
    return Response()


@api_view(["POST"])
def add_ratings(request):
    service.ratings_to_db()
    return Response()


@api_view(["GET"])
def recommend_sources(request):
    user_id = request.data.get("userid")
    try:
        service.validate_userid_input(user_id)
        result = service.recommend_sources(user_id)
    except ValidationError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(result)

