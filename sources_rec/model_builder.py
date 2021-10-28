import tensorflow.keras as keras
import tensorflow as tf
from keras.layers import TextVectorization
import pandas
import numpy
import os
from tensorflow import optimizers
from sklearn.model_selection import train_test_split
from django.db import connection
from sources_rec import models
from stc_sources.settings import BASE_DIR

source_model_file_path = os.path.join(BASE_DIR, "sources_rec/source_model2")

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


class UserModel(tf.keras.Model):
    # ez a Query modell, ide még kéne a topic inputként
    nuser_id = ratings_df.user.nunique()

    def __init__(self):
        super().__init__()

        self.user_embedding = tf.keras.Sequential([
            tf.keras.layers.IntegerLookup(
                vocabulary=self.nuser_id, mask_token=None),
            tf.keras.layers.Embedding(len(self.nuser_id) + 1, 15),
        ])

    def call(self, inputs):
        return self.user_embedding(inputs["user"])


class SourceModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        max_tokens = 10_000

        self.source_topic_vectorizer = TextVectorization(max_tokens=max_tokens)
        self.source_topic_vectorizer.adapt(sources_df["topic"].map(lambda x: x))

        self.source_topic_embedding = tf.keras.Sequential([
            self.source_topic_vectorizer,
            tf.keras.layers.Embedding(max_tokens, 32, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
        ])

    def call(self, inputs):
        return self.source_topic_embedding(inputs["topic"])


def build_recommender_model2():
    ratings_train_set, ratings_test_set = train_test_split(ratings_df, test_size=0.2, random_state=1)
    sources_train_set, sources_test_set = train_test_split(sources_df, test_size=0.2, random_state=1)

    nsource_id = ratings_df.source_id.nunique()
    nuser_id = ratings_df.user.nunique()

    input_sources = keras.layers.Input(shape=[1])
    embed_sources = keras.layers.Embedding(nsource_id + 1, 15)(input_sources)
    sources_out = keras.layers.Flatten()(embed_sources)

    input_users = keras.layers.Input(shape=[1])
    embed_users = keras.layers.Embedding(nuser_id + 1, 15)(input_users)
    users_out = keras.layers.Flatten()(embed_users)

    input_topic = keras.layers.Input(shape=[1])
    source_topic = TextVectorization()
    source_topic.adapt(sources_df["topic"].map(lambda x: x))
    print(source_topic.get_vocabulary())
    source_topic = tf.keras.Sequential([
        tf.keras.layers.TextVectorization(max_tokens=10_000),
        tf.keras.layers.Embedding(10_000, 32, mask_zero=True),
        # We average the embedding of individual words to get one embedding vector
        # per title.
        tf.keras.layers.GlobalAveragePooling1D(),
    ])
    #source_topic_out = keras.layers.Flatten()(source_topic_embedding)

    conc_layer = keras.layers.Concatenate()([sources_out, source_topic_out, users_out])
    x = keras.layers.Dense(128, activation="relu")(conc_layer)
    x_out = keras.layers.Dense(1, activation="relu")(x)
    model = keras.Model([input_sources, input_topic, input_users], x_out)

    opt = optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss="mean_squared_error")

    model.summary()

    hist = model.fit([ratings_train_set.source_id, sources_train_set.topic, ratings_train_set.user],
                     ratings_train_set.rating,
                     batch_size=64,
                     epochs=5,
                     verbose=1,
                     validation_data=([ratings_test_set.source_id, sources_test_set.topic, ratings_test_set.user],
                                      ratings_test_set.rating))

    train_loss = hist.history["loss"]
    val_loss = hist.history["val_loss"]
    print(train_loss)
    print(val_loss)

    model.save(source_model_file_path)
