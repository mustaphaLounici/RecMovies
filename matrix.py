from sklearn.cluster import KMeans
import skfuzzy as fuzz
import numpy as np
import pandas as pd

df = pd.read_csv("./ml-latest-small/ratings.csv")


usersRawIds = np.array(list(set(df["userId"])))
i = 0
in2r_users = {}
r2in_users = {}

for id in usersRawIds:
    in2r_users[i] = id
    r2in_users[id] = i
    i = i+1


def getRawUserId(id):
    return in2r_users[id]


def getInnerUserId(id):
    return r2in_users[id]

# items dict


itemsRawIds = np.array(list(set(df["movieId"])))

i = 0
in2r_items = {}
r2in_items = {}

for id in itemsRawIds:
    in2r_items[i] = id
    r2in_items[id] = i
    i = i+1


def getRawItemsId(id):
    return in2r_items[id]


def getInnerItemsId(id):
    return r2in_items[id]


ratMatrix = np.zeros((len(usersRawIds), len(itemsRawIds)))


for index, row in df.iterrows():
    userId = int(row['userId'])
    itemId = int(row['movieId'])
    rating = row['rating']
    ratMatrix[getInnerUserId(userId), getInnerItemsId(itemId)] = rating

print("matrix done")
# print(ratMatrix[getInnerUserId(1), getInnerItemsId(31)])
# print(ratMatrix[getInnerUserId(669), getInnerItemsId(785)])

# ncenters = 5

# cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
#     ratMatrix, ncenters, 2, error=0.005, maxiter=1000, init=None)

# print("cmeans")
# print(u)
# print(cntr)


# kmeans = KMeans(n_clusters=ncenters, random_state=0).fit(ratMatrix)
# print("kmeans")
# print(kmeans.labels_)
# print(kmeans.cluster_centers_)

# itemsDf = pd.read_csv("./ml-latest-small/movies.csv")


# def mapUserToCategory(userRow):
#     userCategory = {}
#     for i in range(len(userRow)):
#         rating = userRow[i]


# mapUserToCategory(ratMatrix[0])
