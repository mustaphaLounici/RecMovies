from surprise import AlgoBase
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import Reader

import numpy as np
import pandas as pd
import os

from Kmeans import Kmeans
from Cmeans import Cmeans


class MyOwnAlgorithm(AlgoBase):

    def __init__(self):

        # Always call base method before doing anything.
        AlgoBase.__init__(self)

    def fit(self, trainset):

        # Here again: call base method before doing anything.
        AlgoBase.fit(self, trainset)

        adjMatrix = np.zeros(
            (len(trainset.all_users()), len(trainset.all_items())))

        for (userId, itemId, rating) in trainset.all_ratings():
            adjMatrix[userId, itemId] = rating
        self.adjMatrix = adjMatrix

        itemsDf = pd.read_csv("./ml-latest-small/movies.csv")

        def mapUserToCategory(userRow):
            userCategory = {'Adventure': {'ratings': 0.0, 'cmp': 0}, 'Action': {'ratings': 0.0, 'cmp': 0}, 'Animation': {'ratings': 0.0, 'cmp': 0}, "Children": {'ratings': 0.0, 'cmp': 0}, 'Comedy': {'ratings': 0.0, 'cmp': 0}, 'Fantasy': {'ratings': 0.0, 'cmp': 0}, 'Romance': {'ratings': 0.0, 'cmp': 0}, 'Drama': {'ratings': 0.0, 'cmp': 0}, 'Crime': {'ratings': 0.0, 'cmp': 0}, 'Thriller': {
                'ratings': 0.0, 'cmp': 0}, 'Horror': {'ratings': 0.0, 'cmp': 0}, 'Mystery': {'ratings': 0.0, 'cmp': 0}, 'Sci-Fi': {'ratings': 0.0, 'cmp': 0}, 'Documentary': {'ratings': 0.0, 'cmp': 0}, 'IMAX': {'ratings': 0.0, 'cmp': 0}, 'War': {'ratings': 0.0, 'cmp': 0}, 'Musical': {'ratings': 0.0, 'cmp': 0}, 'Western': {'ratings': 0.0, 'cmp': 0}, 'Film-Noir': {'ratings': 0.0, 'cmp': 0}}
            for i in range(len(userRow)):
                rating = userRow[i]
                if rating == 0:
                    continue

                category = itemsDf.loc[itemsDf["movieId"]
                                       == int(trainset.to_raw_iid(i))]

                category = category["genres"].values[0]
                category = category.split('|')

                for cat in category:
                    if cat == "(no genres listed)":
                        continue
                    userCategory[cat]["ratings"] = userCategory[cat]["ratings"] + rating

                    userCategory[cat]["cmp"] = userCategory[cat]["cmp"] + 1

            for cat in userCategory:
                if userCategory[cat]["ratings"] == 0:
                    userCategory[cat] = 0
                else:
                    userCategory[cat] = userCategory[cat]["ratings"] / \
                        userCategory[cat]['cmp']

            return userCategory
        catMatrix = []
        for user in self.adjMatrix:
            catMatrix.append(list(mapUserToCategory(user).values()))
        catMatrix = np.array(catMatrix)
        self.catMatrix = catMatrix

        # # clusturing
        # kmeans = Kmeans(catMatrix)
        # kmeans.plot_calc_best_k()

        cmeans = Cmeans(catMatrix)
        cmeans.plot_calc_best_k()

    def estimate(self, u, i):

        return 3


# path to dataset file
file_path = os.path.expanduser("./ml-latest-small/ratings.csv")

reader = Reader(line_format='user item rating timestamp',
                sep=',', skip_lines=1)

data = Dataset.load_from_file(file_path, reader=reader)

algo = MyOwnAlgorithm()

cross_validate(algo, data, verbose=True, cv=2)
