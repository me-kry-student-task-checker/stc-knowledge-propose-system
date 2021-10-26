from django.test import Client, TestCase
from sources_rec.models import Source, Rating

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

