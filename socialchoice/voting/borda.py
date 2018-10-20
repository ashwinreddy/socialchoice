from .method import Method


class BordaCount(Method):
    """Uses a weighted point system to find a winner that's acceptable for most voters
    """
    def __init__(self, preference_schedule):
        super(BordaCount, self).__init__(preference_schedule)
    
    def _parse_ballot(self, number_of_votes, ballot_order):
        for idx, candidate in enumerate(ballot_order):
            self._points[candidate] += number_of_votes * (self.preference_schedule.number_of_candidates - idx)
