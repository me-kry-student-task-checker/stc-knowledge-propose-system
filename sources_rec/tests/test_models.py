from django.test import TestCase

from sources_rec.models import Source, Rating


class SourceTest(TestCase):

    def setUp(self):
        Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0, ratings_count=0,
                              ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        Source.objects.create(title="Test2", topic="topic2", url="www.proba2.hu", average_rating=0, ratings_count=0,
                              ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)

    def test_sources(self):
        test = Source.objects.get(title="Test")
        test2 = Source.objects.get(title="Test2")
        self.assertEqual(test.topic, "topic")
        self.assertEqual(test2.topic, "topic2")


class RatingTest(TestCase):

    def setUp(self):
        source = Source.objects.create(title="Test", topic="topic", url="www.proba.hu", average_rating=0,
                                       ratings_count=0, ratings_1=0, ratings_2=0, ratings_3=0, ratings_4=0, ratings_5=0)
        Rating.objects.create(source=source, user=1, rating=1)
        Rating.objects.create(source=source, user=2, rating=5)

    def test_ratings(self):
        rating = Rating.objects.get(source=1, user=1)
        rating2 = Rating.objects.get(source=1, user=2)
        self.assertEqual(rating.rating, 1)
        self.assertEqual(rating2.rating, 5)

