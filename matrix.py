from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class RatMatrix:
    def __init__(self, path):
        # reindex users
        self.ratings_df = pd.read_csv(path)
        self.usersRawIds = np.array(
            list(set(self.ratings_df["userId"])))
        i = 0
        self.in2r_users = {}
        self.r2in_users = {}

        for id in self.usersRawIds:
            self.in2r_users[i] = id
            self.r2in_users[id] = i
            i = i+1
        # reindex items
        self.itemsRawIds = np.array(list(set(self.ratings_df["movieId"])))

        i = 0
        self.in2r_items = {}
        self.r2in_items = {}

        for id in self.itemsRawIds:
            self.in2r_items[i] = id
            self.r2in_items[id] = i
            i = i+1

    def getAdjMatrix(self):
        AdjMatrix = np.zeros((len(self.usersRawIds), len(self.itemsRawIds)))
        for _,  row in self.ratings_df.iterrows():
            userId = int(row['userId'])
            itemId = int(row['movieId'])
            rating = row['rating']
            AdjMatrix[self.getInnerUserId(
                userId), self.getInnerItemsId(itemId)] = rating
        self.AdjMatrix = AdjMatrix
        return AdjMatrix

    def getRawItemsId(self, id):
        return self.in2r_items[id]

    def getInnerItemsId(self, id):
        return self.r2in_items[id]

    def getRawUserId(self, id):
        return self.in2r_users[id]

    def getInnerUserId(self, id):
        return self.r2in_users[id]

    def getCategoryMatrix(self, path):
        itemsDf = pd.read_csv(path)

        def mapUserToCategory(userRow):
            userCategory = {'Adventure': {'ratings': 0.0, 'cmp': 0}, 'Action': {'ratings': 0.0, 'cmp': 0}, 'Animation': {'ratings': 0.0, 'cmp': 0}, "Children": {'ratings': 0.0, 'cmp': 0}, 'Comedy': {'ratings': 0.0, 'cmp': 0}, 'Fantasy': {'ratings': 0.0, 'cmp': 0}, 'Romance': {'ratings': 0.0, 'cmp': 0}, 'Drama': {'ratings': 0.0, 'cmp': 0}, 'Crime': {'ratings': 0.0, 'cmp': 0}, 'Thriller': {
                'ratings': 0.0, 'cmp': 0}, 'Horror': {'ratings': 0.0, 'cmp': 0}, 'Mystery': {'ratings': 0.0, 'cmp': 0}, 'Sci-Fi': {'ratings': 0.0, 'cmp': 0}, 'Documentary': {'ratings': 0.0, 'cmp': 0}, 'IMAX': {'ratings': 0.0, 'cmp': 0}, 'War': {'ratings': 0.0, 'cmp': 0}, 'Musical': {'ratings': 0.0, 'cmp': 0}, 'Western': {'ratings': 0.0, 'cmp': 0}, 'Film-Noir': {'ratings': 0.0, 'cmp': 0}}
            for i in range(len(userRow)):
                rating = userRow[i]
                if rating == 0:
                    continue

                category = itemsDf.loc[itemsDf["movieId"]
                                       == self.getRawItemsId(i)]
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
        for user in self.AdjMatrix:
            catMatrix.append(list(mapUserToCategory(user).values()))
        catMatrix = np.array(catMatrix)
        self.catMatrix = catMatrix
        return catMatrix


# ratMatrix = RatMatrix("./ml-latest-small/ratings.csv")
# adjMatrix = ratMatrix.getAdjMatrix()
# catMatrix = ratMatrix.getCategoryMatrix("./ml-latest-small/movies.csv")

# print(adjMatrix)
# print(catMatrix[0])

# adjMatrix = np.loadtxt("./cache/adjMatrix.txt",  delimiter=";")
# print(adjMatrix)
# catMatrix = np.loadtxt("./cache/catMatrix.txt",  delimiter=";")
# # calc best K
# Sum_of_squared_distances = []
# K = range(1, 600)
# for k in K:
#     km = KMeans(n_clusters=k)
#     km = km.fit(np.array(catMatrix))
#     Sum_of_squared_distances.append(km.inertia_)

# plt.plot(K, Sum_of_squared_distances, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Sum_of_squared_distances')
# plt.title('Elbow Method For Optimal k (Kmeans) ')
# plt.show()

# np.savetxt("./cache/adjMatrix.txt", adjMatrix, fmt="%.1f",  delimiter=";")
# np.savetxt("./cache/catMatrix.txt", catMatrix, fmt="%.5f", delimiter=";")
