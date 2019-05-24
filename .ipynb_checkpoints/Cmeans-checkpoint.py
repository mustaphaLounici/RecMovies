import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz


class Cmeans:
    def __init__(self, data):
        self.data = data

    def plot_calc_best_k(self, min=1, max=20):
        Sum_of_squared_distances = []
        K = range(min, max)
        data = np.transpose(np.array(self.data))
        for k in K:
            cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
                data, k, 2, error=0.001, maxiter=900000, init=None)

            Sum_of_squared_distances.append(fpc)
        plt.plot(K, Sum_of_squared_distances, 'bx-')
        plt.xlabel('k')
        plt.ylabel('fpc')
        plt.title('Elbow Method For Optimal k (Cmeans)')
        plt.show()

    def cluster(self, nbrClusters):
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
            self.data, nbrClusters, 2, error=0.001, maxiter=900000, init=None)
        return cntr, u, u0, d, jm, p, fpc
