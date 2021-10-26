from rest_framework.exceptions import ValidationError
import tensorflow.keras as keras
import pandas
import numpy
import os
from django.db import connection
from stc_sources.settings import BASE_DIR
from sources_rec.serializers import SourceSerializer, RatingSerializer
from sources_rec import models


source_model_file_path = os.path.join(BASE_DIR, "sources_rec/source_model")
source_model = keras.models.load_model(source_model_file_path)

query = str(models.Rating.objects.all().query)
ratings_df = pandas.read_sql_query(query, connection)

query = str(models.Source.objects.all().query)
sources_df = pandas.read_sql_query(query, connection)


def recommend_sources(user_id):
    s_id = list(ratings_df.source_id.unique())
    source_arr = numpy.array(s_id)
    user = numpy.array([user_id for i in range(len(s_id))])
    pred = source_model.predict([source_arr, user])

    pred = pred.reshape(-1)
    pred_ids = (-pred).argsort()[0:5]
    recommended_sources = sources_df.iloc[pred_ids]

    returned_sources = []
    for index in recommended_sources.index:
        source = {
            "id": recommended_sources.loc[index, "source_id"],
            "title": recommended_sources.loc[index, "title"],
            "topic": recommended_sources.loc[index, "topic"],
            "url": recommended_sources.loc[index, "url"]
        }
        returned_sources.append(source)

    return {"sources": returned_sources}


def validate_userid_input(user_id):
    if not isinstance(user_id, int) or user_id > len(list(ratings_df.user.unique())) or user_id < 0:
        raise ValidationError


def add_source(source):
    if models.Source.objects.filter(url=source["url"]):
        raise ValidationError
    serializer = SourceSerializer(data=source)
    if serializer.is_valid():
        serializer.save()


def get_sources():
    sources = models.Source.objects.all()
    serializer = SourceSerializer(sources, many=True)
    return serializer.data


def get_source(source_id):
    source = models.Source.objects.get(source_id=source_id)
    serializer = SourceSerializer(source)
    return serializer.data


def delete_source(source_id):
    deleted_source = models.Source.objects.get(source_id=source_id)
    deleted_source.delete()


def update_source(source):
    updated_source = models.Source.objects.filter(source_id=source["source_id"])
    if not updated_source:
        raise ValidationError
    updated_source.update(
        title=source["title"],
        topic=source["topic"],
        url=source["url"]
    )


def add_rating(rating):
    if models.Rating.objects.filter(source=rating["source"], user=rating["user"]):
        raise ValidationError
    serializer = RatingSerializer(data=rating)
    if serializer.is_valid():
        update_source_ratings(rating)
        serializer.save()


def update_source_ratings(rating):
    source = models.Source.objects.get(source_id=rating["source"])
    source.ratings_count = source.ratings_count + 1
    if rating["rating"] == 1:
        source.ratings_1 = source.ratings_1 + 1
    elif rating["rating"] == 2:
        source.ratings_2 = source.ratings_2 + 1
    elif rating["rating"] == 3:
        source.ratings_3 = source.ratings_3 + 1
    elif rating["rating"] == 4:
        source.ratings_4 = source.ratings_4 + 1
    elif rating["rating"] == 5:
        source.ratings_5 = source.ratings_5 + 1
    source.average_rating = (1 * source.ratings_1 + 2 * source.ratings_2 + 3 * source.ratings_3 + 4 * source.ratings_4 +
                             5 * source.ratings_5)/source.ratings_count
    source.save()


def get_user_ratings(user):
    ratings = models.Rating.objects.filter(user=user)
    if not ratings:
        raise ValidationError
    serializer = RatingSerializer(ratings, many=True)
    return serializer.data


def get_source_ratings(source):
    ratings = models.Rating.objects.filter(source=source)
    if not ratings:
        raise ValidationError
    serializer = RatingSerializer(ratings, many=True)
    return serializer.data


def get_source_and_user_ratings(source, user):
    ratings = models.Rating.objects.filter(source=source, user=user)
    if not ratings:
        raise ValidationError
    serializer = RatingSerializer(ratings, many=True)
    return serializer.data


def delete_rating(rating):
    deleted_rating = models.Rating.objects.get(source=rating["source"], user=rating["user"])
    delete_source_ratings(rating, deleted_rating["rating"])
    deleted_rating.delete()


def delete_source_ratings(rating, rating_value):
    source = models.Source.objects.get(source_id=rating["source"])
    source.ratings_count = source.ratings_count - 1
    if rating_value == 1:
        source.ratings_1 = source.ratings_1 - 1
    elif rating_value == 2:
        source.ratings_2 = source.ratings_2 - 1
    elif rating_value == 3:
        source.ratings_3 = source.ratings_3 - 1
    elif rating_value == 4:
        source.ratings_4 = source.ratings_4 - 1
    elif rating_value == 5:
        source.ratings_5 = source.ratings_5 - 1
    source.average_rating = (1 * source.ratings_1 + 2 * source.ratings_2 + 3 * source.ratings_3 + 4 * source.ratings_4 +
                             5 * source.ratings_5) / source.ratings_count
    source.save()


def update_rating(rating):
    updated_rating = models.Rating.objects.filter(source=rating["source"], user=rating["user"])
    if not updated_rating:
        raise ValidationError
    delete_source_ratings(rating, updated_rating["rating"])
    update_source_ratings(rating)
    updated_rating.update(rating=rating["rating"])


"""
source_model_file_path = os.path.join(BASE_DIR, 'calculator_app/source_model')
source_model = keras.models.load_model(source_model_file_path)

sources_file_path = os.path.join(BASE_DIR, 'calculator_app/res/sources.xlsx')
sources = pandas.read_excel(sources_file_path, sheet_name="Sources")
ratings = pandas.read_excel(sources_file_path, sheet_name="Ratings")


def sources_to_db():
    for index in sources.index:
        source = {
            "title": sources.loc[index, "title"],
            "topic": sources.loc[index, "topic"],
            "url": sources.loc[index, "url"],
            "average_rating": sources.loc[index, "average_rating"],
            "ratings_count": sources.loc[index, "ratings_count"],
            "ratings_1": sources.loc[index, "ratings_1"],
            "ratings_2": sources.loc[index, "ratings_2"],
            "ratings_3": sources.loc[index, "ratings_3"],
            "ratings_4": sources.loc[index, "ratings_4"],
            "ratings_5": sources.loc[index, "ratings_5"]
        }
        serializer = SourceSerializer(data=source)
        if serializer.is_valid():
            serializer.save()


def ratings_to_db():
    for index in ratings.index:
        rating = {
            "source": ratings.loc[index, "source_id"],
            "user": ratings.loc[index, "user_id"],
            "rating": ratings.loc[index, "rating"]
        }
        serializer = RatingSerializer(data=rating)
        if serializer.is_valid():
            serializer.save()
"""
