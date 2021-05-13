from sources_rec.serializers import SourceSerializer
import tensorflow.keras as keras
import pandas
import os
from stc_sources.settings import BASE_DIR
from sources_rec.serializers import SourceSerializer, RatingSerializer


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

