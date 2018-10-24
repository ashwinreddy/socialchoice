import numpy as np

class SealedBids(object):
    def __init__(self, bids):
        self.bids = np.array(bids)
    
    @property
    def num_players(self):
        return self.bids.shape[1]
    
    @property
    def settlement(self):
        winners = np.argmax(self.bids, axis=1)
        # print(winners)
        fair_shares = np.sum(self.bids, axis=0) / self.num_players
        # print(fair_shares)
        # how much is each person getting?
        self.items = [ [] for _ in range(self.num_players) ]
        self.value = np.zeros(self.num_players)
        for idx, winner in enumerate(winners):
            self.value[winner] += self.bids[idx][winner]
            self.items[winner].append(idx)
        # print(self.items)
        # what is the surplus
        surplus_per_person = sum(self.value - fair_shares) / self.num_players
        payoffs  = (self.value - fair_shares) - surplus_per_person
        for player in range(self.num_players):
            print("Player {}:".format(player))
            if len(self.items[player]) > 0:
                print("\tGets items".format(player), " and ".join([str(x) for x in self.items[player]]))
            payoff = "$" + str(abs(payoffs[player]))
            if payoffs[player] > 0:
                print("\tPays", payoff)
            elif payoffs[player] < 0:
                print("\tGets", payoff)

        