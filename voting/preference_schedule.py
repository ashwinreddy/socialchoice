import numpy as np

class PreferenceSchedule(object):
    """A wrapper for a preference schedule, which lists the number of votes associated with a preference vote
    """
    def __init__(self, ballot_counts):
        """Turns ballot counts into a numpy matrix and creates a bidirectional map for names and indices in the matrix
        """

        self.candidates_names = set()
        self.votes = []

        # Loop through the keys of the ballot counts
        for ballot in ballot_counts:
            # Applying `list` separates the ballot into the candidates in order
            for candidate in list(ballot):
                # add the candidate's name to the pool of names
                self.candidates_names.add(candidate)

        # make a list of length equal to the number of candidate names
        self.candidates_indices = list(range(len(self.candidates_names)))

        # sort the list of candidate names alphabetically
        self.candidates_names = sorted(list(self.candidates_names))
        
        # build the bidirectional map
        self.name_idx_map = dict(zip(self.candidates_names, self.candidates_indices))
        self.name_idx_map.update(dict(zip(self.candidates_indices, self.candidates_names)))

        # next, tabulate the votes into a matrix
        for ballot in ballot_counts:
            # convert the string ballot into an array of numbers based on the index map
            entry = [self.name_idx_map[candidate] for candidate in list(ballot)]
            # add the number of votes in front
            entry.insert(0, ballot_counts[ballot])
            # add this entry to the votes table
            self.votes.append(entry)

        # build the table and transpose to set it in the correct order
        self.votes = np.array(self.votes)
        
    
    @property
    def number_of_candidates(self):
        return len(self.candidates_names)