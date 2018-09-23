from .method import Method
import numpy as np

class PairwiseComparison(Method):
    def __init__(self, preference_schedule):
        super(PairwiseComparison, self).__init__(preference_schedule)
    
    def _compare_candidates(self, i, j):
        pairwise_votes = {i: 0, j: 0}

        def pairswise_comparison(number_of_votes, ballot_order):
            pairwise_votes[i if np.where(ballot_order == i)[0][0] < np.where(ballot_order == j)[0][0] else j] += number_of_votes
    
        self._loop_through_preferences(pairswise_comparison)

        winner = max(pairwise_votes, key=pairwise_votes.get)
        return winner


    def _compute_ranking(self):
        for i in range(self.preference_schedule.number_of_candidates):
            for j in range(i+1, self.preference_schedule.number_of_candidates):
                winner = self._compare_candidates(i, j)
                self.points[winner] += 1
