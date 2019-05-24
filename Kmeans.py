import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class Kmeans:
    def __init__(self, data):
        self.data = data

    def plot_calc_best_k(self, min=1, max=20):
        Sum_of_squared_distances = []
        K = range(min, max)
        for k in K:
            km = KMeans(n_clusters=k)
            km = km.fit(np.array(self.data))
            Sum_of_squared_distances.append(km.inertia_)

        plt.plot(K, Sum_of_squared_distances, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Sum_of_squared_distances')
        plt.title('Elbow Method For Optimal k (Kmeans) ')
        plt.show()

    def cluster(self, nbrClusters):
        km = KMeans(n_clusters=nbrClusters)
        km = km.fit(np.array(self.data))
        return km
