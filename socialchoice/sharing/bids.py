import numpy as np

class SealedBids(object):
    def __init__(self, bids):
        self.bids = np.array(bids)
    
    @property
    def num_players(self):
        return self.bids.shape[1]
    
    @property
    def settlement(self):
        # for each item, mark the index of the player who bids the most
        winners = np.argmax(self.bids, axis=1)
        # find the total amount each person is bidding and store the equal split among all players
        fair_shares = np.sum(self.bids, axis=0) / self.num_players
        # keeps track of which items each player will get
        self.items = [ [] for _ in range(self.num_players) ]
        # keeps track of how much value each player is getting
        self.value = np.zeros(self.num_players)
        # go through the winners for each item
        for idx, winner in enumerate(winners):
            # if this person wins an item, they get as much value as you valued the item
            self.value[winner] += self.bids[idx][winner]
            # mark that this person got the item
            self.items[winner].append(idx)
        # add up how much each person pays or gets from the estate
        surplus = sum(self.value - fair_shares)
        # divide by all players
        surplus /= self.num_players
        # the payoff is the difference between the value gained and fair share less the surplus
        payoffs  = (self.value - fair_shares) - surplus
        # loop through each player
        for player in range(self.num_players):
            print("Player {}:".format(player))
            # if this person got items
            if len(self.items[player]) > 0:
                # print a listing of their items
                print("\tGets items".format(player), " and ".join([str(x) for x in self.items[player]]))
            # store how much this person pays or gets
            payoff = "$" + str(abs(payoffs[player]))
            # print the person's payoff
            if payoffs[player] > 0:
                print("\tPays", payoff)
            elif payoffs[player] < 0:
                print("\tGets", payoff)

        