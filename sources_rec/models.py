from django.db import models


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    title = models.TextField()
    topic = models.TextField()
    url = models.TextField()
    average_rating = models.FloatField()
    ratings_count = models.IntegerField()
    ratings_1 = models.IntegerField()
    ratings_2 = models.IntegerField()
    ratings_3 = models.IntegerField()
    ratings_4 = models.IntegerField()
    ratings_5 = models.IntegerField()

    class Meta:
        db_table = "sources"


class Rating(models.Model):
    source = models.ForeignKey("Source", on_delete=models.CASCADE)
    user = models.IntegerField()
    rating = models.IntegerField()

    class Meta:
        db_table = "ratings"

