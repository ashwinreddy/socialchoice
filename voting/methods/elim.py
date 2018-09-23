from .method import Method
from .plurality import Plurality
import numpy as np

class PluralityWithElimination(Method):
    def __init__(self, preference_schedule):
        super(PluralityWithElimination, self).__init__(preference_schedule)
        self.plurality_instance = Plurality(self.preference_schedule)
        self.transfers = {idx:idx for idx in range(self.preference_schedule.number_of_candidates)}
        self.ignores = []
    
    def _remove_loser(self, idx):
        found_alternative_to_transfer_to = False
        for preference in self.preference_schedule.votes:
            number_of_votes = preference[0]
            ballot_order = preference[1:]

            if ballot_order[0] == idx:
                found_alternative_to_transfer_to = True
                self.transfers[idx] = ballot_order[1]
                while self.plurality_instance.points[self.transfers[idx]] == float("inf"):
                    self.transfers[idx] = self.transfers[self.transfers[idx]]
                    # print("Oh noes! Points are being transferred to disqualified candidate {}".format(self._idx_to_name(self.transfers[idx])))
                    # print("But that candidate's points were transferred to {}".format(self._idx_to_name( self.transfers[self.transfers[idx]] )))
                    # self.transfers[self.transfers[idx]] 

                self.plurality_instance.points[self.transfers[idx]] += number_of_votes
                self.plurality_instance.points[idx] = float("inf")
        if not found_alternative_to_transfer_to:
            self.ignores.append(idx)
        
    
    def _compute_ranking(self):
        self.plurality_instance._compute_ranking()
        print("Here are the points from the first round of plurality voting:", self.plurality_instance.points)
        for pts in range(self.preference_schedule.number_of_candidates):        
            
            loser_idx = np.argmin(self.plurality_instance.points)

            if loser_idx in self.ignores:
                mins = np.argsort(self.plurality_instance.points, axis=0)
                loser_idx = mins[1]

            print("The loser is {}".format(self._idx_to_name(loser_idx)))
            
            self._remove_loser(loser_idx)
            self.points[loser_idx] = pts
        