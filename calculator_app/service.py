from rest_framework.exceptions import ValidationError
from calculator_app.serializers import CalculationSerializer
import tensorflow.keras as keras
import numpy
import pandas
import os
from calculator.settings import BASE_DIR

model_file_path = os.path.join(BASE_DIR, 'calculator_app/model')
model = keras.models.load_model(model_file_path)

ratings_file_path = os.path.join(BASE_DIR, 'calculator_app/res/ratings.csv')
books_file_path = os.path.join(BASE_DIR, 'calculator_app/res/books.csv')
ratings = pandas.read_csv(ratings_file_path)
books = pandas.read_csv(books_file_path)


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


def calculate(data):
    result = None
    numberA = data["numberA"]
    numberB = data["numberB"]
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

    if not isinstance(data["numberA"], int) and not isinstance(data["numberA"], float):
        raise ValidationError
    elif not isinstance(data["numberB"], int) and not isinstance(data["numberB"], float):
        raise ValidationError
    elif data["operation"] not in operation_list:
        raise ValidationError
    elif data["numberB"] == 0 and data["operation"] == "divide":
        raise ZeroDivisionError


def validate_bookuser_input(user_id):
    if not isinstance(user_id, int) or user_id > len(list(ratings.user_id.unique())):
        raise ValidationError
