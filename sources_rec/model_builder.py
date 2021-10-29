import tensorflow.keras as keras
import tensorflow as tf
import tensorflow_recommenders as tfrs
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

    def call(self, ratings, sources):
        return tf.concat([
            self.user_embedding(ratings["user"]),
            self.source_topic_embedding(sources["topic"])
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
    dataset = tf.data.Dataset.from_tensor_slices(dict(ratings_df))

    def __init__(self):
        super(SourceRecommenderModel, self).__init__()
        # super.__init__(super)
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
                candidates=self.dataset.batch(128).map(self.candidate_model),
            ),
        )

    def compute_loss(self, features, training=False):
        query_embeddings = self.query_model({
            "user": features["user"],
            "timestamp": features["topic"],
        })
        sources_embeddings = self.candidate_model(features["source_id"])

        return self.task(query_embeddings, sources_embeddings)


def build_recommender_model2():
    # Data process to include topic tags in the ratings Dataframe
    topic_column = list()
    for index, row in ratings_df.iterrows():
        source_row = sources_df.loc[sources_df["source_id"] == row["source_id"]]
        topic_column.append(source_row["topic"])

    ratings_df["source_topic"] = topic_column

    cached_train, cached_test = train_test_split(ratings_df, test_size=0.2, random_state=1)
    print(cached_train)
    # cached_train = tf.convert_to_tensor(cached_train, dtype=tf.int32)

    tf.random.set_seed(42)
    #shuffled = ratings_df.shuffle(100_000, seed=42, reshuffle_each_iteration=False)
    shuffled = ratings_df.sample(frac=1)

    train = shuffled.take(80_000)
    test = shuffled.skip(80_000).take(20_000)

    cached_train = train.shuffle(100_000).batch(2048)
    cached_test = test.batch(4096).cache()

    model = SourceRecommenderModel()
    model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))

    model.fit(cached_train, epochs=3)

    train_accuracy = model.evaluate(
        cached_train, return_dict=True)["factorized_top_k/top_100_categorical_accuracy"]
    test_accuracy = model.evaluate(
        cached_test, return_dict=True)["factorized_top_k/top_100_categorical_accuracy"]

    print(f"Top-100 accuracy (train): {train_accuracy:.2f}.")
    print(f"Top-100 accuracy (test): {test_accuracy:.2f}.")

    model.save(source_model_file_path)

    """""
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
    # source_topic_out = keras.layers.Flatten()(source_topic_embedding)

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
    """""
