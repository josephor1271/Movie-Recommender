import os
import string
import sys
import unittest
import csv
import pickle
from contextlib import redirect_stdout

import ps5a as student

with open('expected_output.pkl', 'rb') as pickle_file:
        expected_outputs = pickle.load(pickle_file)

expected_user_to_user_large = expected_outputs['expected_user_to_user_large']
expected_user_to_user_large_genre = expected_outputs['expected_user_to_user_large_genre']
expected_item_to_item_large = expected_outputs['expected_item_to_item_large']
expected_item_to_item_large_genre = expected_outputs['expected_item_to_item_large_genre']
expected_user_to_user_large_predict = expected_outputs['expected_user_to_user_large_predict']
expected_user_to_user_large_predict_genre = expected_outputs['expected_user_to_user_large_predict_genre']
expected_item_to_item_large_predict = expected_outputs['expected_item_to_item_large_predict']
expected_item_to_item_large_predict_genre = expected_outputs['expected_item_to_item_large_predict_genre']

RATINGS_FILENAME = 'ratings.csv'
MOVIES_FILENAME = 'movies.csv'

# A class that inherits from unittest.TestCase, where each function
# is a test you want to run on the student's code. For a full description
# plus a list of all the possible assert methods you can use, see the
# documentation: https://docs.python.org/3/library/unittest.html#unittest.TestCase
class TestEntitiesUsersMovies(unittest.TestCase):
    def setUp(self):
        self.user_id1 = 1
        self.user_id2 = 2
        self.user_id3 = 3
        self.user_name1 = 'Alice'
        self.user_name2 = 'Bob'
        self.user_name3 = 'Carol'

        self.user1 = student.User(self.user_id1, self.user_name1)
        self.user2 = student.User(self.user_id2, self.user_name2)
        self.user3 = student.User(self.user_id3, self.user_name3)

        self.movie_id1 = 1
        self.movie_id2 = 2
        self.movie_id3 = 3
        self.movie_name1 = 'The Lion King'
        self.movie_name2 = 'Air Bud'
        self.movie_name3 = 'Godzilla'
        self.movie_genres1 = ['Adventure', 'Animation', 'Children', 'Drama', 'Musical']
        self.movie_genres2 = ['Children', 'Comedy']
        self.movie_genres3 = ['Action', 'Sci-Fi', 'Thriller']

        self.movie1 = student.Movie(self.movie_id1, self.movie_name1, self.movie_genres1)
        self.movie2 = student.Movie(self.movie_id2, self.movie_name2, self.movie_genres2)
        self.movie3 = student.Movie(self.movie_id3, self.movie_name3, self.movie_genres3)

    def test_user_inheritance(self):
        users = [self.user1, self.user2, self.user3]
        expected_ids = [self.user_id1, self.user_id2, self.user_id3]
        expected_names = [self.user_name1, self.user_name2, self.user_name3]

        for user, expected_id in zip(users, expected_ids):
            self.assertEqual(expected_id, user.get_id(),
                f"The User's get_id() returns {user.get_id()} not {expected_id}. Are you calling the super constructor?")

        for user, expected_name in zip(users, expected_names):
            self.assertEqual(expected_name, user.get_name(),
                f"The User's get_name() returns {user.get_name()} not {expected_name}. Are you calling the super constructor?")

    def test_movie_inheritance(self):
        movies = [self.movie1, self.movie2, self.movie3]
        expected_ids = [self.movie_id1, self.movie_id2, self.movie_id3]
        expected_names = [self.movie_name1, self.movie_name2, self.movie_name3]

        for movie, expected_id in zip(movies, expected_ids):
            self.assertEqual(expected_id, movie.get_id(),
                f"The Movie's get_id() returns {movie.get_id()} not {expected_id}. Are you calling the super constructor?")

        for movie, expected_name in zip(movies, expected_names):
            self.assertEqual(expected_name, movie.get_name(),
                f"The Movie's get_name() returns {movie.get_name()} not {expected_name}. Are you calling the super constructor?")

    def test_movie_get_genres(self):
        response = self.movie1.get_genres()
        self.assertEqual(response, self.movie_genres1,
                         "get_genres returned %s, but %s was expected" % (response, self.movie_genres1))
        response = self.movie2.get_genres()
        self.assertEqual(response, self.movie_genres2,
                         "get_genres returned %s, but %s was expected" % (response, self.movie_genres2))
        response = self.movie3.get_genres()
        self.assertEqual(response, self.movie_genres3,
                         "get_genres returned %s, but %s was expected" % (response, self.movie_genres2))

class TestRecommenderBase(unittest.TestCase):
    def setUp(self):
        self.user1 = student.User(1, 'Alice')
        self.user2 = student.User(2, 'Bob')
        self.user3 = student.User(3, 'Carol')

        self.movie1 = student.Movie(1, 'Toy Story', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy'])
        self.movie2 = student.Movie(2, 'The Lion King', ['Adventure', 'Animation', 'Children', 'Drama', 'Musical'])
        self.movie3 = student.Movie(3, 'Mission Impossible', ['Action', 'Adventure', 'Mystery', 'Thriller'])
        self.movie4 = student.Movie(4, 'Air Bud', ['Children', 'Comedy'])
        self.movie5 = student.Movie(5, 'Godzilla', ['Action', 'Sci-Fi', 'Thriller'])

        self.small_recommender = student.Recommender()

    def test_recommender_base_add_rating(self):
        self.small_recommender.add_rating(self.user1, self.movie1, 5)
        self.small_recommender.add_rating(self.user1, self.movie2, 4)
        self.small_recommender.add_rating(self.user2, self.movie1, 4)

        self.assertEqual(self.small_recommender.user_to_movies[self.user1][self.movie1], 5,
                        "add_rating does not add the correct rating value to user_to_movies.")
        self.assertEqual(self.small_recommender.user_to_movies[self.user1][self.movie2], 4,
                        "add_rating does not add the correct rating value to user_to_movies.")
        self.assertEqual(self.small_recommender.user_to_movies[self.user2][self.movie1], 4,
                        "add_rating does not add the correct rating value to user_to_movies.")

        self.assertEqual(self.small_recommender.movie_to_users[self.movie1][self.user1], 5,
                        "add_rating does not add the correct rating value to movie_to_users.")
        self.assertEqual(self.small_recommender.movie_to_users[self.movie2][self.user1], 4,
                        "add_rating does not add the correct rating value to movie_to_users.")
        self.assertEqual(self.small_recommender.movie_to_users[self.movie1][self.user2], 4,
                        "add_rating does not add the correct rating value to movie_to_users.")

    def test_recommender_base_add_rating_duplicate(self):
        self.small_recommender.add_rating(self.user1, self.movie1, 5)

        with self.assertRaises(ValueError, msg='Duplicate rating should raise a ValueError.'):
            self.small_recommender.add_rating(self.user1, self.movie1, 3)

    def test_recommender_base_get_user_ratings(self):
        self.small_recommender.add_rating(self.user1, self.movie1, 5)
        self.small_recommender.add_rating(self.user1, self.movie2, 4)
        self.small_recommender.add_rating(self.user1, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie1, 4)
        self.small_recommender.add_rating(self.user2, self.movie2, 4)
        self.small_recommender.add_rating(self.user2, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie4, 4)
        self.small_recommender.add_rating(self.user2, self.movie5, 5)
        self.small_recommender.add_rating(self.user3, self.movie1, 4)
        self.small_recommender.add_rating(self.user3, self.movie2, 5)
        self.small_recommender.add_rating(self.user3, self.movie3, 3)
        self.small_recommender.add_rating(self.user3, self.movie4, 3)
        self.small_recommender.add_rating(self.user3, self.movie5, 2)

        expected1 = {self.movie1: 5, self.movie2: 4, self.movie3: 4}
        expected2 = {self.movie1: 4, self.movie2: 4, self.movie3: 4, self.movie4: 4, self.movie5: 5}
        expected3 = {self.movie1: 4, self.movie2: 5, self.movie3: 3, self.movie4: 3, self.movie5: 2}

        response = self.small_recommender.get_user_ratings(self.user1)
        self.assertEqual(response, expected1,
                         "get_user_ratings returned %s, but %s was expected" % (response, expected1))
        response = self.small_recommender.get_user_ratings(self.user2)
        self.assertEqual(response, expected2,
                         "get_user_ratings returned %s, but %s was expected" % (response, expected2))
        response = self.small_recommender.get_user_ratings(self.user3)
        self.assertEqual(response, expected3,
                         "get_user_ratings returned %s, but %s was expected" % (response, expected3))

    def test_recommender_base_get_movie_ratings(self):
        self.small_recommender.add_rating(self.user1, self.movie1, 5)
        self.small_recommender.add_rating(self.user1, self.movie2, 4)
        self.small_recommender.add_rating(self.user1, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie1, 4)
        self.small_recommender.add_rating(self.user2, self.movie2, 4)
        self.small_recommender.add_rating(self.user2, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie4, 4)
        self.small_recommender.add_rating(self.user2, self.movie5, 5)
        self.small_recommender.add_rating(self.user3, self.movie1, 4)
        self.small_recommender.add_rating(self.user3, self.movie2, 5)
        self.small_recommender.add_rating(self.user3, self.movie3, 3)
        self.small_recommender.add_rating(self.user3, self.movie4, 3)
        self.small_recommender.add_rating(self.user3, self.movie5, 2)

        expected1 = {self.user1: 5, self.user2: 4, self.user3: 4}
        expected2 = {self.user1: 4, self.user2: 4, self.user3: 5}
        expected4 = {self.user2: 4, self.user3: 3}

        response = self.small_recommender.get_movie_ratings(self.movie1)
        self.assertEqual(response, expected1,
                         "get_movie_ratings returned %s, but %s was expected" % (response, expected1))
        response = self.small_recommender.get_movie_ratings(self.movie2)
        self.assertEqual(response, expected2,
                         "get_movie_ratings returned %s, but %s was expected" % (response, expected2))
        response = self.small_recommender.get_movie_ratings(self.movie4)
        self.assertEqual(response, expected4,
                         "get_movie_ratings returned %s, but %s was expected" % (response, expected4))

def load_data(movies_file, ratings_file, recommender, num_users=None):
    users = {}
    movies = {}
    processed_users = set()

    with open(movies_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie_id = int(row['movieId'])
            name = row['title']
            genres = row['genres'].split('|') if row['genres'] != '(no genres listed)' else []
            movie = student.Movie(movie_id, name, genres)
            movies[movie_id] = movie

    with open(ratings_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = int(row['userId'])
            name = row['firstName']

            if user_id not in processed_users:
                users[user_id] = student.User(user_id, name)
                processed_users.add(user_id)

            if num_users is not None and len(processed_users) > num_users:
                break

            movie_id = int(row['movieId'])
            rating = float(row['rating'])

            movie = movies.get(movie_id)
            if movie:
                recommender.add_rating(users[user_id], movie, rating)

class TestUserToUserRecommender(unittest.TestCase):
    # Helper function to check if two dictionaries are equal within a range; ripped from https://stackoverflow.com/questions/50935269/assertalmostequal-for-a-value-in-a-dict
    def assertDictAlmostEqual(self, d1, d2, msg=None, places=7):
        # check if both inputs are dicts
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')

        # check if both inputs have the same keys
        self.assertEqual(d1.keys(), d2.keys())

        # check each key
        for key, value in d1.items():
            if isinstance(value, tuple):
                self.assertAlmostEqual(d1[key][0], d2[key][0], places=places, msg=msg)
                self.assertAlmostEqual(d1[key][1], d2[key][1], places=places, msg=msg)
            else:
                self.assertAlmostEqual(d1[key], d2[key], places=places, msg=msg)

    def setUp(self):
        self.user1 = student.User(1, 'Alice')
        self.user2 = student.User(2, 'Bob')
        self.user3 = student.User(3, 'Carol')

        self.movie1 = student.Movie(1, 'Toy Story', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy'])
        self.movie2 = student.Movie(2, 'The Lion King', ['Adventure', 'Animation', 'Children', 'Drama', 'Musical'])
        self.movie3 = student.Movie(3, 'Mission Impossible', ['Action', 'Adventure', 'Mystery', 'Thriller'])
        self.movie4 = student.Movie(4, 'Air Bud', ['Children', 'Comedy'])
        self.movie5 = student.Movie(5, 'Godzilla', ['Action', 'Sci-Fi', 'Thriller'])

        self.small_recommender = student.UserToUserRecommender()
        self.small_recommender.add_rating(self.user1, self.movie1, 5)
        self.small_recommender.add_rating(self.user1, self.movie2, 4)
        self.small_recommender.add_rating(self.user1, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie1, 4)
        self.small_recommender.add_rating(self.user2, self.movie2, 4)
        self.small_recommender.add_rating(self.user2, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie4, 4)
        self.small_recommender.add_rating(self.user2, self.movie5, 5)
        self.small_recommender.add_rating(self.user3, self.movie1, 4)
        self.small_recommender.add_rating(self.user3, self.movie2, 5)
        self.small_recommender.add_rating(self.user3, self.movie3, 3)
        self.small_recommender.add_rating(self.user3, self.movie4, 3)
        self.small_recommender.add_rating(self.user3, self.movie5, 2)

        self.large_recommender = student.UserToUserRecommender()
        load_data(MOVIES_FILENAME, RATINGS_FILENAME, self.large_recommender, 20)

    def test_user_to_user_weights_and_ratings_small(self):
        expected = {self.movie4: [(0.9941348467724342, 4), (0.9740492440449617, 3)], self.movie5: [(0.9941348467724342, 5), (0.9740492440449617, 2)]}
        response = self.small_recommender.collect_weights_and_ratings(self.user1)
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the user-to-user recommender returned %s, but %s was expected" % (response, expected))

    def test_user_to_user_weights_and_ratings_small_genre(self):
        expected = {self.movie4: [(0.9941348467724342, 4), (0.9740492440449617, 3)]}
        response = self.small_recommender.collect_weights_and_ratings(self.user1, genre='Comedy')
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the user-to-user recommender with the genre parameter toggled returned %s, but %s was expected" % (response, expected))

    def test_user_to_user_weights_and_ratings_large(self):
        expected = expected_user_to_user_large
        response = self.large_recommender.collect_weights_and_ratings(self.large_recommender.find_user(17))
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the user-to-user recommender does not return the correct dictionary for a large recommender")

    def test_user_to_user_weights_and_ratings_large_genre(self):
        expected = expected_user_to_user_large_genre
        response = self.large_recommender.collect_weights_and_ratings(self.large_recommender.find_user(17), genre='Romance')
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the user-to-user recommender with genre toggled does not return the correct dictionary for a large recommender")

class TestItemToItemRecommender(unittest.TestCase):
    # Helper function to check if two dictionaries are equal within a range; ripped from https://stackoverflow.com/questions/50935269/assertalmostequal-for-a-value-in-a-dict
    def assertDictAlmostEqual(self, d1, d2, msg=None, places=7):
        # check if both inputs are dicts
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')

        # check if both inputs have the same keys
        self.assertEqual(d1.keys(), d2.keys())

        # check each key
        for key, value in d1.items():
            if isinstance(value, tuple):
                self.assertAlmostEqual(d1[key][0], d2[key][0], places=places, msg=msg)
                self.assertAlmostEqual(d1[key][1], d2[key][1], places=places, msg=msg)
            else:
                self.assertAlmostEqual(d1[key], d2[key], places=places, msg=msg)

    def setUp(self):
        self.user1 = student.User(1, 'Alice')
        self.user2 = student.User(2, 'Bob')
        self.user3 = student.User(3, 'Carol')

        self.movie1 = student.Movie(1, 'Toy Story', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy'])
        self.movie2 = student.Movie(2, 'The Lion King', ['Adventure', 'Animation', 'Children', 'Drama', 'Musical'])
        self.movie3 = student.Movie(3, 'Mission Impossible', ['Action', 'Adventure', 'Mystery', 'Thriller'])
        self.movie4 = student.Movie(4, 'Air Bud', ['Children', 'Comedy'])
        self.movie5 = student.Movie(5, 'Godzilla', ['Action', 'Sci-Fi', 'Thriller'])

        self.small_recommender = student.ItemToItemRecommender()
        self.small_recommender.add_rating(self.user1, self.movie1, 5)
        self.small_recommender.add_rating(self.user1, self.movie2, 4)
        self.small_recommender.add_rating(self.user1, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie1, 4)
        self.small_recommender.add_rating(self.user2, self.movie2, 4)
        self.small_recommender.add_rating(self.user2, self.movie3, 4)
        self.small_recommender.add_rating(self.user2, self.movie4, 4)
        self.small_recommender.add_rating(self.user2, self.movie5, 5)
        self.small_recommender.add_rating(self.user3, self.movie1, 4)
        self.small_recommender.add_rating(self.user3, self.movie2, 5)
        self.small_recommender.add_rating(self.user3, self.movie3, 3)
        self.small_recommender.add_rating(self.user3, self.movie4, 3)
        self.small_recommender.add_rating(self.user3, self.movie5, 2)

        self.large_recommender = student.ItemToItemRecommender()
        load_data(MOVIES_FILENAME, RATINGS_FILENAME, self.large_recommender, 20)

    def test_item_to_item_weights_and_ratings_small(self):
        expected = {self.movie4: [(0.9899494936611665, 5), (0.9682773237093576, 4), (1.0, 4)], self.movie5: [(0.9191450300180578, 5), (0.8700221858486124, 4), (0.9656157585206697, 4)]}
        response = self.small_recommender.collect_weights_and_ratings(self.user1)
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the item-to-item recommender returned %s, but %s was expected" % (response, expected))

    def test_item_to_item_weights_and_ratings_small_genre(self):
        expected = {self.movie4: [(0.9899494936611665, 5), (0.9682773237093576, 4), (1.0, 4)]}
        response = self.small_recommender.collect_weights_and_ratings(self.user1, genre='Comedy')
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the item-to-item recommender with the genre parameter toggled returned %s, but %s was expected" % (response, expected))

    def test_item_to_item_weights_and_ratings_large(self):
        expected = expected_item_to_item_large
        response = self.large_recommender.collect_weights_and_ratings(self.large_recommender.find_user(17))
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the item-to-item recommender does not return the correct dictionary for a large recommender")

    def test_item_to_item_weights_and_ratings_large_genre(self):
        expected = expected_item_to_item_large_genre
        response = self.large_recommender.collect_weights_and_ratings(self.large_recommender.find_user(17), genre='Romance')
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "collect_weights_and_ratings for the item-to-item recommender with genre toggled does not return the correct dictionary for a large recommender")

class TestRecommenderComplete(unittest.TestCase):
    # Helper function to check if two dictionaries are equal within a range; ripped from https://stackoverflow.com/questions/50935269/assertalmostequal-for-a-value-in-a-dict
    def assertDictAlmostEqual(self, d1, d2, msg=None, places=7):
        # check if both inputs are dicts
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')

        # check if both inputs have the same keys
        self.assertEqual(d1.keys(), d2.keys())

        # check each key
        for key, value in d1.items():
            if isinstance(value, tuple):
                self.assertAlmostEqual(d1[key][0], d2[key][0], places=places, msg=msg)
                self.assertAlmostEqual(d1[key][1], d2[key][1], places=places, msg=msg)
            else:
                self.assertAlmostEqual(d1[key], d2[key], places=places, msg=msg)

    def setUp(self):
        self.large_u_recommender = student.UserToUserRecommender()
        load_data(MOVIES_FILENAME, RATINGS_FILENAME, self.large_u_recommender, 20)

        self.large_i_recommender = student.ItemToItemRecommender()
        load_data(MOVIES_FILENAME, RATINGS_FILENAME, self.large_i_recommender, 20)

    def test_recommender_complete_predict_ratings_large(self):
        expected = expected_user_to_user_large_predict
        response = self.large_u_recommender.predict_ratings(self.large_u_recommender.find_user(17))
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "predict_ratings does not return the correct dictionary for a large recommender")

        expected = expected_item_to_item_large_predict
        response = self.large_i_recommender.predict_ratings(self.large_i_recommender.find_user(17))
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "predict_ratings does not return the correct dictionary for a large recommender")

    def test_recommender_complete_predict_ratings_large_genre(self):
        expected = expected_user_to_user_large_predict_genre
        response = self.large_u_recommender.predict_ratings(self.large_u_recommender.find_user(17), genre='Romance')
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "predict_ratings with genre toggled does not return the correct dictionary for a large recommender")

        expected = expected_item_to_item_large_predict_genre
        response = self.large_i_recommender.predict_ratings(self.large_i_recommender.find_user(17), genre='Romance')
        response = {user.get_id(): rating for user, rating in response.items()}
        self.assertDictAlmostEqual(response, expected,
                         "predict_ratings with genre toggled does not return the correct dictionary for a large recommender")

    def test_recommender_complete_recommend_large(self):
        expected = ['Akira (1988)', 'Animal House (1978)', 'Big Short, The (2015)', 'Blood Diamond (2006)', 'Client, The (1994)']
        response = self.large_u_recommender.recommend(self.large_u_recommender.find_user(17), 5)
        self.assertEqual(response, expected,
                         "recommend does not return the correct list of movies for a large recommender, returned %s, but %s was expected" % (response, expected))

        expected = ['About a Boy (2002)', 'Indian in the Cupboard, The (1995)', 'Logan (2017)', 'Star Trek II: The Wrath of Khan (1982)', 'Wallace & Gromit: The Best of Aardman Animation (1996)']
        response = self.large_i_recommender.recommend(self.large_i_recommender.find_user(17), 5)
        self.assertEqual(response, expected,
                         "recommend does not return the correct list of movies for a large recommender, returned %s, but %s was expected" % (response, expected))

    def test_recommender_complete_recommend_large_genre(self):
        expected = ['English Patient, The (1996)', 'Postman, The (Postino, Il) (1994)', 'Sunset Blvd. (a.k.a. Sunset Boulevard) (1950)']
        response = self.large_u_recommender.recommend(self.large_u_recommender.find_user(17), 3, genre='Romance')
        self.assertEqual(response, expected,
                         "recommend with genre toggled does not return the correct list of movies for a large recommender, returned %s, but %s was expected" % (response, expected))

        expected = ['About a Boy (2002)', 'Fisher King, The (1991)', 'Postman, The (Postino, Il) (1994)']
        response = self.large_i_recommender.recommend(self.large_i_recommender.find_user(17), 3, genre='Romance')
        self.assertEqual(response, expected,
                         "recommend with genre toggled does not return the correct list of movies for a large recommender, returned %s, but %s was expected" % (response, expected))

# Dictionary mapping function names from the above TestCase class to
# the point value each test is worth.
point_values = {
    'test_user_inheritance': .1,
    'test_movie_inheritance': .1,
    'test_movie_get_genres': .1,
    'test_recommender_base_add_rating': .2,
    'test_recommender_base_add_rating_duplicate': .1,
    'test_recommender_base_get_user_ratings': .2,
    'test_recommender_base_get_movie_ratings': .2,
    'test_user_to_user_weights_and_ratings_small': .25,
    'test_user_to_user_weights_and_ratings_small_genre': .25,
    'test_user_to_user_weights_and_ratings_large': .25,
    'test_user_to_user_weights_and_ratings_large_genre': .25,
    'test_item_to_item_weights_and_ratings_small': .25,
    'test_item_to_item_weights_and_ratings_small_genre': .25,
    'test_item_to_item_weights_and_ratings_large': .25,
    'test_item_to_item_weights_and_ratings_large_genre': .25,
    'test_recommender_complete_predict_ratings_large': .5,
    'test_recommender_complete_predict_ratings_large_genre': .5,
    'test_recommender_complete_recommend_large': .5,
    'test_recommender_complete_recommend_large_genre': .5
}

# Subclass to track a point score and appropriate
# grade comment for a suit of unit tests
class Results_600(unittest.TextTestResult):

    # We override the init method so that the Result object
    # can store the score and appropriate test output.
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 5

    def addFailure(self, test, err):
        test_name = test._testMethodName
        msg = str(err[1])
        self.handleDeduction(test_name, msg)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, None)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, message):
        point_value = point_values[test_name]
        if message is None:
            message = 'Your code produced an error on test %s.' % test_name
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= point_value

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points


if __name__ == '__main__':
    print('Running Unit Tests!')
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEntitiesUsersMovies))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRecommenderBase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUserToUserRecommender))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestItemToItemRecommender))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRecommenderComplete))


    result = unittest.TextTestRunner(
        verbosity=2, resultclass=Results_600).run(suite)

    output = result.getOutput()
    points = result.getPoints()

    if points < .1:
        points = 0

    print("\nProblem Set 4B Unit Test Results:")
    print(output)
    print("Points: %s/5\n" % points)
