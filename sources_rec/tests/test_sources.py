from django.test import TestCase, Client
from django.urls import reverse

from sources_rec.models import Source
from sources_rec.serializers import SourceSerializer

client = Client()


class GetAllSourcesTest(TestCase):

    def setUp(self):
        Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0, ratings_count=0,
                              ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        Source.objects.create(title="Test2", topic="topic2", url="www.proba2.hu", average_rating=0, ratings_count=0,
                              ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)

    def test_get_all_sources(self):
        response = client.get(reverse("get_sources"))
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        self.assertEqual(response.data, serializer.data)
