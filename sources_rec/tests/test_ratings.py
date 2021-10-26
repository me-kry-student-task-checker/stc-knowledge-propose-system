from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from sources_rec.models import Source, Rating
from sources_rec.serializers import RatingSerializer, SourceSerializer

client = Client()


class GetRatingsTest(TestCase):

    def setUp(self):
        self.source1 = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=3,
                                             ratings_count=2,
                                             ratings_1=1, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=1)
        self.source2 = Source.objects.create(title="Test2", topic="topic", url="www.proba2.hu", average_rating=3,
                                             ratings_count=1,
                                             ratings_1=0, ratings_2=0, ratings_3=1, ratings_4=0, ratings_5=0)
        self.rating1 = Rating.objects.create(source=self.source1, user=1, rating=1)
        self.rating2 = Rating.objects.create(source=self.source1, user=2, rating=5)
        self.rating3 = Rating.objects.create(source=self.source2, user=1, rating=3)

    def test_get_user_ratings(self):
        user = {
            "user": 1
        }
        response = client.post(reverse("get_user_ratings"), data=user, content_type="application/json")
        ratings = Rating.objects.filter(user=user["user"])
        serializer = RatingSerializer(ratings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_ratings_invalid_input(self):
        user = {
            "user": "1"
        }
        response = client.post(reverse("get_user_ratings"), data=user, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invalid_user_ratings(self):
        user = {
            "user": 3
        }
        response = client.post(reverse("get_user_ratings"), data=user, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_source_ratings(self):
        source = {
            "source": self.source1.pk
        }
        response = client.post(reverse("get_source_ratings"), data=source, content_type="application/json")
        ratings = Rating.objects.filter(source=source["source"])
        serializer = RatingSerializer(ratings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_source_ratings_invalid_input(self):
        source = {
            "source": "4"
        }
        response = client.post(reverse("get_source_ratings"), data=source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invalid_source_ratings(self):
        source = {
            "source": -1
        }
        response = client.post(reverse("get_source_ratings"), data=source, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_source_and_user_ratings(self):
        data = {
            "source": self.source1.pk,
            "user": 1
        }
        response = client.post(reverse("get_source_and_user_ratings"), data=data, content_type="application/json")
        ratings = Rating.objects.filter(source=data["source"], user=data["user"])
        serializer = RatingSerializer(ratings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_source_and_user_ratings_invalid_input(self):
        data = {
            "source": "Test",
            "user": 1
        }
        response = client.post(reverse("get_source_and_user_ratings"), data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invalid_source_and_user_ratings(self):
        data = {
            "source": -1,
            "user": 1
        }
        response = client.post(reverse("get_source_and_user_ratings"), data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddRatingTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=3,
                                             ratings_count=2,
                                             ratings_1=1, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=1)
        self.rating1 = Rating.objects.create(source=self.source, user=1, rating=1)
        self.rating2 = Rating.objects.create(source=self.source, user=2, rating=5)

    def test_add_rating(self):
        rating = {
            "source": self.source.pk,
            "user": 3,
            "rating": 3,
        }
        response = client.post(reverse("add_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        source = Source.objects.get(source_id=self.source.pk)
        serializer = SourceSerializer(source)
        self.assertEqual(serializer.data["ratings_3"], 1)
        self.assertEqual(serializer.data["ratings_count"], 3)
        self.assertEqual(serializer.data["average_rating"], 3)

    def test_add_rating_invalid_input_type(self):
        rating = {
            "source": self.source.pk,
            "user": "3",
            "rating": 3,
        }
        response = client.post(reverse("add_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rating_invalid_source(self):
        rating = {
            "source": -1,
            "user": 3,
            "rating": 3,
        }
        response = client.post(reverse("add_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rating_invalid_user(self):
        rating = {
            "source": self.source.pk,
            "user": 1,
            "rating": 3,
        }
        response = client.post(reverse("add_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rating_invalid_user(self):
        rating = {
            "source": self.source.pk,
            "user": 3,
            "rating": 6,
        }
        response = client.post(reverse("add_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRatingTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=3,
                                             ratings_count=2,
                                             ratings_1=1, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=1)
        self.rating1 = Rating.objects.create(source=self.source, user=1, rating=1)
        self.rating2 = Rating.objects.create(source=self.source, user=2, rating=5)

    def test_delete_rating(self):
        rating = {
            "source": self.source.pk,
            "user": 1
        }
        response = client.delete(reverse("delete_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        source = Source.objects.get(source_id=self.source.pk)
        serializer = SourceSerializer(source)
        self.assertEqual(serializer.data["ratings_1"], 0)
        self.assertEqual(serializer.data["ratings_count"], 1)
        self.assertEqual(serializer.data["average_rating"], 5)

    def test_delete_rating_invalid_input(self):
        rating = {
            "source": self.source.pk,
            "user": "1"
        }
        response = client.delete(reverse("delete_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_rating_invalid_source(self):
        rating = {
            "source": -1,
            "user": 1
        }
        response = client.delete(reverse("delete_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_rating_invalid_user(self):
        rating = {
            "source": self.source.pk,
            "user": -1
        }
        response = client.delete(reverse("delete_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateRatingTest(TestCase):

    def setUp(self):
        self.source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=3,
                                             ratings_count=2,
                                             ratings_1=1, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=1)
        self.rating1 = Rating.objects.create(source=self.source, user=1, rating=1)
        self.rating2 = Rating.objects.create(source=self.source, user=2, rating=5)

    def test_update_rating(self):
        rating = {
            "source": self.source.pk,
            "user": 1,
            "rating": 5,
        }
        response = client.put(reverse("update_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        source = Source.objects.get(source_id=self.source.pk)
        serializer = SourceSerializer(source)
        self.assertEqual(serializer.data["ratings_1"], 0)
        self.assertEqual(serializer.data["ratings_5"], 2)
        self.assertEqual(serializer.data["ratings_count"], 2)
        self.assertEqual(serializer.data["average_rating"], 5)

    def test_update_rating_invalid_input_type(self):
        rating = {
            "source": self.source.pk,
            "user": "1",
            "rating": 5,
        }
        response = client.put(reverse("update_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_rating_invalid_rating_value(self):
        rating = {
            "source": self.source.pk,
            "user": 1,
            "rating": 6,
        }
        response = client.put(reverse("update_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_rating_invalid_source(self):
        rating = {
            "source": -1,
            "user": 1,
            "rating": 5,
        }
        response = client.put(reverse("update_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_rating_invalid_user(self):
        rating = {
            "source": self.source.pk,
            "user": 3,
            "rating": 5,
        }
        response = client.put(reverse("update_rating"), data=rating, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

