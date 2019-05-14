from surprise import AlgoBase
from surprise import Dataset
from surprise.model_selection import cross_validate
import numpy as np


class MyOwnAlgorithm(AlgoBase):

    def __init__(self):

        # Always call base method before doing anything.
        AlgoBase.__init__(self)

    def fit(self, trainset):

        # Here again: call base method before doing anything.
        AlgoBase.fit(self, trainset)
        # print(trainset)
        # Compute the average rating. We might as well use the
        # trainset.global_mean attribute ;)
        self.the_mean = np.mean([r for (_, _, r) in
                                 self.trainset.all_ratings()])

        return self

    def estimate(self, u, i):

        return 4


data = Dataset.load_builtin('ml-100k')

algo = MyOwnAlgorithm()

cross_validate(algo, data, verbose=True)
