import tensorflow.keras as keras
import pandas
import numpy
import os
from tensorflow import optimizers
from sklearn.model_selection import train_test_split
from django.db import connection
from sources_rec import models
from stc_sources.settings import BASE_DIR


source_model_file_path = os.path.join(BASE_DIR, "sources_rec/source_model")

query = str(models.Rating.objects.all().query)
ratings_df = pandas.read_sql_query(query, connection)

query = str(models.Source.objects.all().query)
sources_df = pandas.read_sql_query(query, connection)


def build_recommender_model():
    train_set, test_set = train_test_split(ratings_df, test_size=0.2, random_state=1)

    nsource_id = ratings_df.source_id.nunique()
    nuser_id = ratings_df.user.nunique()

    input_sources = keras.layers.Input(shape=[1])
    embed_sources = keras.layers.Embedding(nsource_id + 1, 15)(input_sources)
    sources_out = keras.layers.Flatten()(embed_sources)

    input_users = keras.layers.Input(shape=[1])
    embed_users = keras.layers.Embedding(nuser_id + 1, 15)(input_users)
    users_out = keras.layers.Flatten()(embed_users)

    conc_layer = keras.layers.Concatenate()([sources_out, users_out])
    x = keras.layers.Dense(128, activation="relu")(conc_layer)
    x_out = x = keras.layers.Dense(1, activation="relu")(x)
    model = keras.Model([input_sources, input_users], x_out)

    opt = optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss="mean_squared_error")

    model.summary()

    hist = model.fit([train_set.source_id, train_set.user], train_set.rating,
                     batch_size=64,
                     epochs=5,
                     verbose=1,
                     validation_data=([test_set.source_id, test_set.user], test_set.rating))

    train_loss = hist.history["loss"]
    val_loss = hist.history["val_loss"]
    print(train_loss)
    print(val_loss)

    model.save(source_model_file_path)
