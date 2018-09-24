from .method import Method

class Plurality(Method):
    """This class implements vanilla plurality algorithm.

    Plurality is the basic algorithm most people are familiar with. Whoever earns the most first-place votes wins.
    """
    def __init__(self, preference_schedule):
        super(Plurality, self).__init__(preference_schedule)
    
    def _parse_ballot(self, number_of_votes, ballot_order):
        """Analyzes this ballot to give the first place winner all the votes
        """
        first_place_winner = ballot_order[0] # the first person on the ballot is the first place winner
        self.points[first_place_winner] += number_of_votes # add the number of votes to their point tabulation
