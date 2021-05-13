from rest_framework.decorators import api_view
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

