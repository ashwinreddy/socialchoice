import unittest
import socialchoice

math_club_election = {'ABCD': 14, 'CBDA': 10, 'DCBA': 8, 'BDCA': 4, 'CDBA': 1}

class TestPlurality(unittest.TestCase):
    method = socialchoice.voting.Plurality

    def test_two_candidate(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule({'ABC': 1, 'BCA': 2})).winner, 'B')

    def test_tsu_marching_band(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule({'RHFOS': 49, 'HSOFR': 48, 'FHSOR': 3})).winner, 'R')

class TestBordaCount(unittest.TestCase):
    method = socialchoice.voting.BordaCount

    def test_two_candidate(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule({'ABC': 1, 'BCA': 2})).winner, 'B')

    def test_math_club_election(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule(math_club_election)).winner, 'B')

class TestPairwise(unittest.TestCase):
    method = socialchoice.voting.PairwiseComparison

    def test_two_candidate(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule({'ABC': 1, 'BCA': 2})).winner, 'B')


class TestPluralityWithElimination(unittest.TestCase):
    method = socialchoice.voting.PluralityWithElimination

    def test_two_candidate(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule({'ABC': 1, 'BCA': 2})).winner, 'B')
    
    def test_math_club_election(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule(math_club_election)).winner, 'D')
    
    def test_kingsburg_mayoral_election(self):
        self.assertEqual(self.method(socialchoice.PreferenceSchedule({'ABCDE': 93, 'BDECA': 44, 'CAEBD': 10, 'CEBAD': 30, 'DCEAB': 42, 'EDCBA': 81})).winner, 'E')

if __name__ == "__main__":
    unittest.main()