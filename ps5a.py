import math

class Entity(object):
    def __init__(self, id, name):
        """
        Initializes an Entity object.

        id (int): an integer representing the user or movie ID
        name (str): a string representing the user or movie name

        An Entity has two attributes:
            - its id
            - its name
        """
        self.id = id
        self.name = name

    def get_id(self):
        """
        Used to access the entity's id outside of the class.

        Returns (int): the entity's id
        """
        return self.id

    def get_name(self):
        """
        Used to access the entity's name outside of the class.

        Returns (str): the entity's name
        """
        return self.name

    def __hash__(self):
        """
        Computes a unique hash value based on the entity's id and name.

        Returns (int): the hash value for the entity
        """
        # Do NOT modify this method!
        return hash((str(self.id), self.name))


class User(Entity):
    def __init__(self, user_id, name):
        """
        Initializes a User object which inherits from Entity.

        user_id (integer): an integer representing the user ID
        name (str): a string representing the user's first name
        """
        Entity.__init__(self, user_id, name)



class Movie(Entity):
    def __init__(self, movie_id, name, genres):
        """
        Initializes a Movie object which inherits from Entity.

        movie_id (integer): an integer representing the movie ID
        name (str): a string representing the movie's title
        genres (list[str]): a list of strings of the genres the movie is categorized under
        """
        Entity.__init__(self, movie_id, name)
        self.genres = genres

    def get_genres(self):
        """
        Used to access the movie's genre list outside of the class.

        Returns (list[str]): the list of genres the movie falls under
        """
        return self.genres


class Recommender(object):
    """
    A Recommender object stores users and movies in a bidirectional lookup table, maintaining two dictionaries as attributes:
            1. user_to_movies (dict): a dictionary mapping a User object to a dictionary of movies and their ratings
            - key: User object
            - value: dictionary where keys are Movie objects and values are ratings (int) given by the user
            2. movie_to_users (dict): a dictionary mapping a Movie object to a dictionary of users and their ratings
            - key: Movie object
            - value: dictionary where keys are User objects and values are ratings (int) given by the user to the movie
    """

    def __init__(self):
        """
        Initializes a Recommender object with two empty dictionaries.
            - user_to_movies (dict)
            - movie_to_users (dict)
        """
        self.user_to_movies = {}
        self.movie_to_users = {}

    def add_rating(self, user, movie, rating):
        """
        Adds a rating for a user-movie pair if the user-movie pair is not already in the recommender.
        Raises a ValueError if the user has already rated the movie.

        user (User object): the user rating the movie
        movie (Movie object): the movie being rated by the user
        rating (int): the rating for the movie (between 1 and 5, inclusive)
        """
       # Initialize user and movie entries if they don't exist
        if user not in self.user_to_movies:
            self.user_to_movies[user] = {}
        if movie not in self.movie_to_users:
            self.movie_to_users[movie] = {}

        # Check if the user has already rated the movie
        if movie in self.user_to_movies[user]:
            raise ValueError("User has already rated this movie.")

        # Add the rating
        self.user_to_movies[user][movie] = rating
        self.movie_to_users[movie][user] = rating


    def get_user_ratings(self, user):
        """
        Returns a copy of the dictionary of all ratings given by a given user.
        The keys of this dictionary should be movies and the values are the ratings the user gave to the movies.

        user (User object): the user whose ratings are being accessed

        Returns (dict): a COPY of the dictionary of all ratings given by the user
        """
        return self.user_to_movies[user].copy()


    def get_movie_ratings(self, movie):
        """
        Returns a copy of the dictionary of all ratings received by a given movie.
        The keys of this dictionary should be users and the values are the ratings those users gave to the movie.

        movie (Movie object): the movie whose ratings are being accessed

        Returns (dict): a COPY of the dictionary of all ratings received by the movie
        """
        return self.movie_to_users[movie].copy()

    def find_user(self, user_id):
        """
        Returns a User object given a user ID.

        user_id (int): the ID of the user to return

        Returns (User object): the User object with the given ID
        """
        # Do NOT modify this method!
        return [user for user in self.user_to_movies.keys() if user.get_id() == user_id][0]

    def calculate_similarity(self, ratings1, ratings2):
        """
        Calculates the cosine similarity between two users or two movies based on their ratings.

        ratings1 (dict): a dictionary of ratings for a particular user or movie
        ratings2 (dict): a dictionary of ratings for another user or movie

        Returns (float): the similarity score between the two ratings dictionaries
        """
        # Do NOT modify this method!
        shared = [i for i in ratings1 if i in ratings2]
        if not shared:
            return 0

        numerator = sum([ratings1[i] * ratings2[i] for i in shared])
        denominator = math.sqrt(sum([ratings1[i] ** 2 for i in shared]) * sum([ratings2[i] ** 2 for i in shared]))

        return numerator / denominator

    def collect_weights_and_ratings(self, target_user, genre=None):
        """
        Collects the weights and ratings needed to calculate predictions for each movie.

        target_user (User object): the user for whom to collect weights and ratings for recommendations
        genre (str): the genre to filter movies by (by default None: all movies are considered)

        Returns (dict): keys are movies the user has not rated and values are lists of tuples of weights and ratings
        """
        # Do NOT modify this method! — Implement in subclasses.
        raise NotImplementedError

    def predict_ratings(self, target_user, genre=None):
        """
        Predicts ratings for movies that a user has not yet rated by taking a weighted average of ratings for other movies.
        The weights and ratings for prediction calculation are determined by the collect_weights_and_ratings method.

        target_user (User object): the user for whom to predict ratings
        genre (str): the genre to filter movies by (by default None: all movies are considered)

        Returns (dict): keys are movies the user has not rated and values are the predicted ratings for the user
        """
        weights_and_ratings = self.collect_weights_and_ratings(target_user, genre)
        predicted_ratings = {}
        for unwatched_movie in weights_and_ratings.keys():
            numerator = 0
            denominator = 0
            tuple_list = weights_and_ratings[unwatched_movie]
            for pair in tuple_list:
                numerator += pair[0] * pair[1]
                denominator += pair[0]
            try:
                predicted_ratings[unwatched_movie] = numerator/denominator
            except ZeroDivisionError:
                predicted_ratings[unwatched_movie] = 0
        return predicted_ratings




    def recommend(self, target_user, num_recommendations, genre=None):
        """
        Recommends a specified number of movies to a particular user based on the highest predicted ratings.
        If fewer than num_recommendations movies are available, return all available movies.
        Sorts the recommended movies in descending order of predicted ratings. Ties are broken by sorting in alphabetical order.

        target_user (User object): the user for whom to predict ratings
        num_recommendations (int): the number of recommendations to return
        genre (str): the genre to filter movies by (by default None: all movies are considered)

        Returns (list): a list of Item names to recommend to the user, sorted from highest to lowest predicted rating
        """
        predicted_ratings = self.predict_ratings(target_user, genre)

        redicted_ratings = self.predict_ratings(target_user, genre)

        # Create a list of (movie_name, predicted_rating) tuples
        recs = [(movie.name, rating) for movie, rating in predicted_ratings.items()]


        # Sort by predicted rating (descending) and then by movie name (ascending)
        recs.sort(key=lambda x: (-x[1], x[0]))

        # Return the top num_recommendations movies
        return [rec[0] for rec in recs[:num_recommendations]]



class UserToUserRecommender(Recommender):
    def collect_weights_and_ratings(self, target_user, genre=None):
        """
        Collects the weights and ratings needed to calculate predictions for each movie.
        Determines similarity scores used for weighting the ratings with the user-to-user collaborative filtering approach
        by comparing target user ratings with other users.

        target_user (User object): the user for whom to collect weights and ratings for recommendations
        genre (str): the genre to filter movies by (by default None: all movies are considered)

        Returns (dict): keys are movies the user has not rated and values are lists of tuples of weights and ratings
        """
        #get the rating of target user
        target_user_ratings = self.get_user_ratings(target_user)
        unrated = []
        #list of movies user has not rated/seen
        for movie in self.movie_to_users.copy():
            if target_user not in self.get_movie_ratings(movie) and genre == None:
                unrated.append(movie)
            elif target_user not in self.get_movie_ratings(movie) and genre in movie.get_genres():
                unrated.append(movie)
        #initialize return dictionary
        weights_ratings = {}
        #for every unrated movie,
        for movie in unrated:
            #make entry in dictionary as movie:[]
            weights_ratings[movie] = []
            #for every user who has watched the movie,
            for user in self.get_movie_ratings(movie).keys():
                #get the users ratings
                user_ratings = self.get_user_ratings(user)
                #calculate similarity between user and target user
                sim_score = self.calculate_similarity(user_ratings, target_user_ratings)
                rating = self.get_movie_ratings(movie)[user]
                weights_ratings[movie].append((sim_score, rating))
                #now each entry is movie:[(sim_score0, user0_rating), (sim_score1, user1_rating)...]
        return weights_ratings



class ItemToItemRecommender(Recommender):
    def collect_weights_and_ratings(self, target_user, genre=None):
        """
        Collects the weights and ratings needed to calculate predictions for each movie.
        Determines similarity scores used for weighting the ratings with the item-to-item collaborative filtering approach
        by comparing unrated movies with movies target user has rated.

        target_user (User object): the user for whom to collect weights and ratings for recommendations
        genre (str): the genre to filter movies by (by default None: all movies are considered)

        Returns (dict): keys are movies the user has not rated and values are lists of tuples of weights and ratings
        """


        unrated = []
        #list of movies user has not rated/seen

        for movie in self.movie_to_users.copy():
            if target_user not in self.get_movie_ratings(movie) and genre == None:
                unrated.append(movie)
            elif target_user not in self.get_movie_ratings(movie) and genre in movie.get_genres():
                unrated.append(movie)
        #initialize return dictionary
        weights_ratings = {}
        #for every uwatched movie,
        for unwatched_movie in unrated:
            #make entry in dictionary as movie:[]
            weights_ratings[unwatched_movie] = []
            #get other peoples rating for unwatched movies
            unwatched_ratings = self.get_movie_ratings(unwatched_movie)
            #for every movie target user has seen,
            for watched_movie in self.get_user_ratings(target_user).keys():
                #get everyones rating for watched movies
                watched_ratings = self.get_movie_ratings(watched_movie)
                #calculate similarity between unawatched movie rankings and watched movie rankiings
                sim_score = self.calculate_similarity(unwatched_ratings, watched_ratings)
                rating = self.get_movie_ratings(watched_movie)[target_user]
                weights_ratings[unwatched_movie].append((sim_score, rating))
                #now each entry is movie:[(sim_score0, movie0_rating), (sim_score1, movie1_rating)...]
        return weights_ratings

if __name__ == "__main__":
    pass
