from .method import Method
import numpy as np

class PairwiseComparison(Method):
    def __init__(self, preference_schedule):
        super(PairwiseComparison, self).__init__(preference_schedule)
    
    def _compare_candidates(self, i, j):
        """Compares candidates i and j as if no other candidates existed
        """
        # a table to keep track of who has how many points for this 1-on-1 comparison
        pairwise_votes = {i: 0, j: 0}

        def pairswise_comparison(number_of_votes, ballot_order):
            winner = i if np.where(ballot_order == i)[0][0] < np.where(ballot_order == j)[0][0] else j
            pairwise_votes[winner] += number_of_votes
    
        # loop through all preferences, using the voting scheme of all points going to the more liked candidate on each ballot
        self._loop_through_preferences(pairswise_comparison)

        # do an argmax on the table and return that candidate's index
        winner = max(pairwise_votes, key=pairwise_votes.get)
        return winner


    def compute_ranking(self):
        # pit every possible combination of two candidates with each other
        for i in range(self.preference_schedule.number_of_candidates):
            for j in range(i+1, self.preference_schedule.number_of_candidates):
                # compare the candidates
                winner = self._compare_candidates(i, j)
                # give the point to the winner of the comparison
                self._points[winner] += 1
