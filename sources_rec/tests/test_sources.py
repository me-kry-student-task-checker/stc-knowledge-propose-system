from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from sources_rec.models import Source
from sources_rec.serializers import SourceSerializer

client = Client()


class GetSourcesTest(TestCase):

    def setUp(self):
        self.source1 = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0,
                                             ratings_count=0,
                                             ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        self.source2 = Source.objects.create(title="Test2", topic="topic2", url="www.proba2.hu", average_rating=0,
                                             ratings_count=0,
                                             ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)

    def test_get_all_sources(self):
        response = client.get(reverse("get_sources"))
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_one_valid_source(self):
        source = {
            "source": self.source1.pk
        }
        response = client.post(reverse("get_source"), data=source, content_type="application/json")
        source = Source.objects.get(url=self.source1.url)
        serializer = SourceSerializer(source)
        self.assertEqual(response.data, serializer.data)

    def test_get_one_invalid_source(self):
        source = {
            "source": -1
        }
        response = client.post(reverse("get_source"), data=source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_one_source_invalid_input(self):
        source = {
            "source": ""
        }
        response = client.post(reverse("get_source"), data=source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddSourceTest(TestCase):

    def setUp(self):
        self.starting_source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0,
                                             ratings_count=0,
                                             ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        self.empty_source = {
            "title": "",
            "topic": "Topic",
            "url": "www.test.hu"
        }
        self.invalid_type_source = {
            "title": "Test",
            "topic": "Topic",
            "url": 34
        }
        self.existing_source = {
            "title": "Title",
            "topic": "Topic",
            "url": "www.proba.hu"
        }
        self.valid_source = {
            "title": "Title",
            "topic": "Topic",
            "url": "www.test.hu"
        }

    def test_add_empty_source(self):
        response = client.post(reverse("add_source"), data=self.empty_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_invalid_type_source(self):
        response = client.post(reverse("add_source"), data=self.invalid_type_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_existing_source(self):
        response = client.post(reverse("add_source"), data=self.existing_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_valid_source(self):
        response = client.post(reverse("add_source"), data=self.valid_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeleteSourceTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0,
                                         ratings_count=0,
                                         ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        self.valid_source = {
            "source": self.source.pk
        }
        self.invalid_source = {
            "source": -1
        }

    def test_delete_source(self):
        response = client.delete(reverse("delete_source"), data=self.valid_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_invalid_source(self):
        response = client.delete(reverse("delete_source"), data=self.invalid_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSourceTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0,
                                            ratings_count=0,
                                            ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        self.valid_source = {
            "source_id": self.source.pk,
            "title": "New title",
            "topic": "New topic",
            "url": "www.new.hu",
        }
        self.invalid_type_source = {
            "source_id": self.source.pk,
            "title": 2,
            "topic": "New topic",
            "url": "www.new.hu",
        }
        self.invalid_source = {
            "source_id": -1,
            "title": "New title",
            "topic": "New topic",
            "url": "www.new.hu",
        }

    def test_update_source(self):
        response = client.put(reverse("update_source"), data=self.valid_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_source_invalid_input(self):
        response = client.put(reverse("update_source"), data=self.invalid_type_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_source(self):
        response = client.put(reverse("update_source"), data=self.invalid_source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

