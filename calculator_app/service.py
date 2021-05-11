from rest_framework.exceptions import ValidationError
from calculator_app.serializers import CalculationSerializer
import tensorflow.keras as keras
import numpy
import pandas
import os
from stc_sources.settings import BASE_DIR

'''
model_file_path = os.path.join(BASE_DIR, 'calculator_app/model')
model = keras.models.load_model(model_file_path)

ratings_file_path = os.path.join(BASE_DIR, 'calculator_app/res/ratings.csv')
books_file_path = os.path.join(BASE_DIR, 'calculator_app/res/books.csv')
ratings = pandas.read_csv(ratings_file_path)
books = pandas.read_csv(books_file_path)
'''

source_model_file_path = os.path.join(BASE_DIR, 'calculator_app/source_model')
source_model = keras.models.load_model(source_model_file_path)

sources_file_path = os.path.join(BASE_DIR, 'calculator_app/res/sources.xlsx')
sources = pandas.read_excel(sources_file_path, sheet_name="Sources")
sources_ratings = pandas.read_excel(sources_file_path, sheet_name="Ratings")

'''
def recommend_books(user_id):
    b_id = list(ratings.book_id.unique())
    book_arr = numpy.array(b_id)
    user = numpy.array([user_id for i in range(len(b_id))])
    predication = model.predict([book_arr, user])

    predication = predication.reshape(-1)
    predicated_bookids = (-predication).argsort()[0:5]
    recommended_books = books.iloc[predicated_bookids]

    recommended_books = recommended_books[["book_id", "title", "authors"]].to_json(orient="records")
    return recommended_books
'''


def recommend_sources(user_id):
    s_id = list(sources_ratings.source_id.unique())
    source_arr = numpy.array(s_id)
    user = numpy.array([user_id for i in range(len(s_id))])
    pred = source_model.predict([source_arr, user])

    pred = pred.reshape(-1)
    pred_ids = (-pred).argsort()[0:5]
    recommended_sources = sources.iloc[pred_ids]

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


def calculate(data):
    result = None
    numberA = data["numbera"]
    numberB = data["numberb"]
    operation = data["operation"]

    if operation == "add":
        result = numberA + numberB
    elif operation == "minus":
        result = numberA - numberB
    elif operation == "multiple":
        result = numberA * numberB
    elif operation == "divide":
        result = numberA / numberB

    data["result"] = result
    serializer = CalculationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    return {"result": result}


def validate_input(data):
    operation_list = ["add", "minus", "multiple", "divide"]

    if not isinstance(data["numbera"], int) and not isinstance(data["numbera"], float):
        raise ValidationError
    elif not isinstance(data["numberb"], int) and not isinstance(data["numberb"], float):
        raise ValidationError
    elif data["operation"] not in operation_list:
        raise ValidationError
    elif data["numberb"] == 0 and data["operation"] == "divide":
        raise ZeroDivisionError


def validate_bookuser_input(user_id):
    if not isinstance(user_id, int) or user_id > len(list(ratings.user_id.unique())) or user_id < 0:
        raise ValidationError


def validate_sourceuser_input(user_id):
    if not isinstance(user_id, int) or user_id > len(list(sources_ratings.user_id.unique())) or user_id < 0:
        raise ValidationError
