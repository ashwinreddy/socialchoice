from .method import Method
from .plurality import Plurality
import numpy as np

class PluralityWithElimination(Method):
    def __init__(self, preference_schedule):
        self.preference_schedule = preference_schedule
        self._points = np.zeros(self.preference_schedule.number_of_candidates)
        # plurality with elimination uses plurality as a base implementation
        self.plurality_instance = Plurality(self.preference_schedule)
        # this dictionary keeps track of which candidate's votes get transferred where
        # for now, everyone's votes map to themselves
        self.transfers = {idx:idx for idx in range(self.preference_schedule.number_of_candidates)}
        # a list of candidates whose votes have nowhere to go
        self.ignores = []
    
    
    def compute_ranking(self):
        # First use plurality to generate a simple ranking
        self.plurality_instance.compute_ranking()
        # Now, we eliminate each candidate, and the number of points they get is equal to the order in which they are eliminated
        # That is, 0th person eliminated gets 0 points, 1st gets 1, and so on and so forth.
        for pts in range(self.preference_schedule.number_of_candidates):
            # do an argmin on the points to find the person with the fewest first place votes ("loser")
            loser_idx = np.argmin(self.plurality_instance._points)

            # print("Loser found: {}".format(self._idx_to_name(loser_idx)))

            # HACK: this bit tries to deal with the fact that our loser might not have anyone to transfer points to
            mins = np.argsort(self.plurality_instance._points, axis=0)
            idx = 1
            while loser_idx in self.ignores:
                # print("These are the list of losers: ", self.ignores)
                loser_idx = mins[idx]
                idx += 1
            
            # we remove this loser from the race
            self._remove_loser(loser_idx)
            # give them their points
            self._points[loser_idx] = pts
    
    def _remove_loser(self, idx):
        found_alternative_to_transfer_to = False
        # loop through all the ballots
        for preference in self.preference_schedule.votes:
            number_of_votes = preference[0]
            ballot_order = preference[1:]

            # if the winner of this ballot is our loser
            if ballot_order[0] == idx:
                # print("The winner of this ballot is the plurality loser {}".format(self._idx_to_name(idx)))
                found_alternative_to_transfer_to = True
                # then we record that we will be transferring their points to the 2nd place on that ballot
                # print("The second place winner is {}".format(self._idx_to_name(ballot_order[1])))
                self.transfers[idx] = ballot_order[1]
                # print("Here are the transfer protocols", [ '=>'.join((self._idx_to_name(key), self._idx_to_name(self.transfers[key]))) for key in self.transfers])
                # if the person we are transferring to has been eliminated,
                while self.plurality_instance._points[self.transfers[idx]] == float("inf"):
                    # then we should really be transferring the points to whomever that eliminated 2nd place candidate was transferring their votes to
                    self.transfers[idx] = self.transfers[self.transfers[idx]]

                # we give the person who deserves those votes after the loser those votes
                self.plurality_instance._points[self.transfers[idx]] += number_of_votes
                # and eliminate this candidate
                self.plurality_instance._points[idx] = float("inf")
        # if we couldn't find anyone to whom the votes could be given
        if not found_alternative_to_transfer_to:
            # silence this candidate from appearing in computations in the future
            self.ignores.append(idx)
        
        