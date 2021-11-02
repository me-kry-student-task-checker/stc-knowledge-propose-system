from rest_framework import serializers
import sources_rec.models as models


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = ("source_id", "title", "topic", "url", "average_rating", "ratings_count",
                  "ratings_1", "ratings_2", "ratings_3", "ratings_4", "ratings_5")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ("source", "user", "rating")
