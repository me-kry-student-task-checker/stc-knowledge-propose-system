import tensorflow.keras as keras
import tensorflow as tf
import tensorflow_recommenders as tfrs
from keras.layers import TextVectorization
import pandas
import os
from tensorflow import optimizers
from sklearn.model_selection import train_test_split
from django.db import connection
from sources_rec import models
from stc_sources.settings import BASE_DIR


source_model_file_path = os.path.join(BASE_DIR, "sources_rec/source_model")

ratings_query = str(models.Rating.objects.all().query)
ratings_df = pandas.read_sql_query(ratings_query, connection)

sources_query = str(models.Source.objects.all().query)
sources_df = pandas.read_sql_query(sources_query, connection)

topic_column = list()
for index, row in ratings_df.iterrows():
    source_row = sources_df.loc[sources_df["source_id"] == row["source_id"]]
    topic_column.append(source_row["topic"].iloc[0])

ratings_df["source_topic"] = topic_column

"""""
ratings_ds = (
    tf.data.Dataset.from_tensor_slices(
        (
            tf.cast(ratings_df["source_id"].values, tf.int32),
            tf.cast(ratings_df["user"].values, tf.int32),
            tf.cast(ratings_df["rating"].values, tf.int32),
            tf.cast(ratings_df["source_topic"].values, tf.string)
        )
    )
)

sources_ds = (
    tf.data.Dataset.from_tensor_slices(
        (
            tf.cast(sources_df["source_id"].values, tf.int32),
            tf.cast(sources_df["title"].values, tf.string),
            tf.cast(sources_df["topic"].values, tf.string),
            tf.cast(sources_df["url"].values, tf.string),
            tf.cast(sources_df["average_rating"].values, tf.float32),
            tf.cast(sources_df["ratings_count"].values, tf.int32),
            tf.cast(sources_df["ratings_1"].values, tf.int32),
            tf.cast(sources_df["ratings_2"].values, tf.int32),
            tf.cast(sources_df["ratings_3"].values, tf.int32),
            tf.cast(sources_df["ratings_4"].values, tf.int32),
            tf.cast(sources_df["ratings_5"].values, tf.int32)
        )
    )
)
"""""


def prepare_fresh_data():
    global ratings_df
    global sources_df
    ratings_df = pandas.read_sql_query(ratings_query, connection)
    sources_df = pandas.read_sql_query(sources_query, connection)

    topic_column = list()
    for index, row in ratings_df.iterrows():
        source_row = sources_df.loc[sources_df["source_id"] == row["source_id"]]
        topic_column.append(source_row["topic"].iloc[0])

    ratings_df["source_topic"] = topic_column
    print(ratings_df)


def build_recommender_model():
    prepare_fresh_data()
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
    x_out = keras.layers.Dense(1, activation="relu")(x)
    model = keras.Model([input_sources, input_users], x_out)

    opt = optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss="mean_squared_error")

    model.summary()

    hist = model.fit([train_set.source_id, train_set.user], train_set.rating,
                     batch_size=32,
                     epochs=5,
                     verbose=1,
                     validation_data=([test_set.source_id, test_set.user], test_set.rating))

    train_loss = hist.history["loss"]
    val_loss = hist.history["val_loss"]
    print(train_loss)
    print(val_loss)

    model.save(source_model_file_path)

"""""
class UserModel(tf.keras.Model):
    nuser_id = ratings_df.user.nunique()

    def __init__(self):
        super().__init__()

        self.user_embedding = keras.Sequential([
            tf.keras.layers.IntegerLookup(
                vocabulary=ratings_df["user"].unique(), mask_token=None),
            tf.keras.layers.Embedding(self.nuser_id + 1, 15),
        ])

        max_tokens = 10_000

        self.source_topic_vectorizer = TextVectorization(max_tokens=max_tokens)
        self.source_topic_vectorizer.adapt(sources_df["topic"].map(lambda x: x))

        self.source_topic_embedding = keras.Sequential([
            self.source_topic_vectorizer,
            tf.keras.layers.Embedding(max_tokens, 32, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
        ])

    def call(self, inputs):
        return tf.concat([
            self.user_embedding(inputs["user"]),
            self.source_topic_embedding(inputs["source_topic"])
        ], axis=1)


class SourceModel(tf.keras.Model):
    nsource_id = ratings_df.source_id.nunique()

    def __init__(self):
        super().__init__()

        self.source_embedding = keras.Sequential([
            tf.keras.layers.IntegerLookup(
                vocabulary=ratings_df["source_id"].unique(), mask_token=None),
            tf.keras.layers.Embedding(self.nsource_id + 1, 15),
        ])

    def call(self, ratings):
        return self.source_embedding(ratings["source_id"])


class SourceRecommenderModel(tfrs.models.Model):

    def __init__(self):
        super(SourceRecommenderModel, self).__init__()
        self.query_model = keras.Sequential([
            UserModel(),
            tf.keras.layers.Dense(32)
        ])
        self.candidate_model = keras.Sequential([
            SourceModel(),
            tf.keras.layers.Dense(32)
        ])
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                # nem jó
                candidates=sources_ds.batch(128).map(self.candidate_model),
            ),
        )

    def compute_loss(self, features, training=False):
        query_embeddings = self.query_model({
            "user": features["user"],
            "topic": features["topic"],
        })
        sources_embeddings = self.candidate_model(features["source_id"])

        return self.task(query_embeddings, sources_embeddings)
"""
