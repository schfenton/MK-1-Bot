import random


class Poll:
    """Class representing a poll with the ability to add candidates and votes, then calculate the total. Takes in
    optional candidate list argument."""

    def __init__(self, candidates, randomized_winner=False):
        self._candidates = candidates
        self._votes = []
        self._open = False
        self._random = randomized_winner
        self._results = None

    def open(self):
        """Sets poll to open. Votes cannot be accepted until the poll is open. Candidates cannot be added/removed
        while poll is open. Results will be reset if the poll is opened after closing."""
        self._results = None
        if len(self._candidates) == 0:
            raise PollError("No candidates in poll")
        elif len(self._candidates) == 1:
            raise PollError("No opponents to candidate")
        else:
            self._open = True

    def close(self):
        """Closes poll and calculates and saves the result to results variable. Returns the results."""
        if len(self.get_votes()) == 0:  # If there are no votes
            raise PollError("No votes to count")
        self._open = False  # Close poll
        self._results = {
            "winner": None,
            "tied": None
        }

        votes = self.get_votes()
        vote_sums = [0] * len(self.get_candidates())
        for vote in votes:  # Sum scores across all votes for each candidate
            for i in range(0, len(self.get_candidates())):
                vote_sums[i] += vote[i]

        highest_score_candidates = find_max_index(vote_sums)  # Find index (or indices) of highest scored candidate(s)
        finalists = []
        for i in range(len(highest_score_candidates)):  # check both first and second finalists
            if len(highest_score_candidates[i]) > 1:  # If there is more than one candidate with the highest score...
                # Break by comparing in ranking (may be multiple indices if another tie)
                highest_rank = self.compare_rank(highest_score_candidates[i])
                if len(highest_rank) > 1:  # if there are still multiple with same rank (true tie)
                    pick = 0
                    if self._random:
                        pick = random.randrange(len(highest_rank))  # if random, pick a random index
                    finalists.append(highest_rank[pick])  # choose picked candidate index as the finalist
                else:  # otherwise there is one candidate with highest rank
                    finalists.append(highest_rank[0])  # choose them as finalist
            else:  # otherwise there is one candidate with the highest score, so assign them as finalist
                finalists.append(highest_score_candidates[i][0])

        # Find highest rank out of the two highest scoring candidates
        highest_rank_candidates = self.compare_rank(finalists)
        if len(highest_rank_candidates) > 1:
            # if a tie between highest ranked, find index of highest scoring candidates out of the highest ranked
            max_score = find_max_index([vote_sums[candidate] for candidate in highest_rank_candidates])[0]
            if len(max_score) > 1:
                # if there are multiple highest ranked candidates with highest scores...
                winner = 0
                if self._random:
                    # if randomized winner True, choose a random index from the ties as winner
                    winner = random.randrange(len(max_score))
                # pop winner out of max_score
                self._results['winner'] = self.get_candidates()[max_score.pop(winner)]
                # # log other candidates (who tied) in results
                # self._results['tied'] = [self.get_candidates()[candidate] for candidate in max_score]
            else:
                # otherwise the winner of the ranked tie is the candidate with the highest score
                self._results['winner'] = self._candidates[max_score[0]]
        else:  # if there isn't a tie between the highest ranked, the winner is the highest ranked candidate
            self._results['winner'] = self._candidates[highest_rank_candidates[0]]

        return self.get_results()

    def compare_rank(self, candidates: list):
        """For internal use counting votes. Tally how many voters score each candidate higher given by indexes in
        list. Returns highest candidate as index in list, or multiple indexes if candidates tie."""
        if len(candidates) == 1:
            return [candidates[0]]
        votes = self.get_votes()
        tally = [0] * len(candidates)
        for vote in votes:  # vote: [#, #, #, #, #]
            favored = find_max_index([vote[index] for index in candidates])
            # list comprehension to isolate scores of candidates wanted

            for candidate in favored[0]:
                tally[candidate] += 1  # add one to tally for highest scoring candidate (if multiple tie add to all)

        high_rank = find_max_index(tally)[0]
        return [candidates[i] for i in high_rank]  # list with index of highest tally (or mult. if tie)
        # ^ might have issue since find_max_index return data changed

    def is_open(self):
        """Returns True if poll is open, False otherwise."""
        return self._open

    def get_results(self):
        """Returns results."""
        return self._results

    # def add_candidates(self, candidate):
    #     """Takes candidates as list of strings and appends to poll's candidate list. Can only be used
    #     if the poll is not open."""
    #
    # def remove_candidates(self, candidate):
    #     """Takes candidates as list of strings and removes from poll's candidate list. Can only be used if
    #     the poll is not open."""

    def get_candidates(self):
        """Returns list of current candidates."""
        return self._candidates

    def add_vote(self, scores):
        """Takes voter's scores and appends to list of votes for later calculation. Order of list must match
        order of candidates. Returns index of submission in votes."""
        if not self.is_open():
            raise PollError("Poll is not open for voting")
        if not isinstance(scores, list):  # error if scores is not a list
            raise TypeError("Scores must be submitted as a list of integers between 0 and 5")
        for score in scores:  # error if any score is...
            if not isinstance(score, int):  # not an integer
                raise TypeError("Scores must be submitted as a list of integers between 0 and 5")
            if score not in range(0, 6):  # not between 0 and 5
                raise TypeError("Scores must be submitted as a list of integers between 0 and 5")
        if len(scores) != len(self.get_candidates()):  # error if scores do not match the number of candidates
            raise PollError("Amount of scores not equal to amount of candidates")

        self._votes.append(scores)  # add list of scores to votes
        return len(self._votes) - 1

    # def remove_vote(self, voter, scores):

    def get_votes(self):
        return self._votes


def find_max_index(values: list):
    """For internal use calculating the total, takes in a list of integers and returns the indexes of the highest
    two numbers in values nested in a two-value list."""
    order = []
    for cycle in range(2):
        max_i = None
        for i in range(0, len(values)):
            if cycle == 1 and i in order[0]:
                break
            if not max_i:
                max_i = [i]
            elif values[i] > values[max_i[0]]:
                max_i = [i]
            elif values[i] == values[max_i[0]]:
                max_i.append(i)
        if max_i:
            order.append(max_i)
    return order


class PollError(Exception):
    """Exception raised for logical errors during poll functions."""

    def __init__(self, message):
        self.message = message

    pass


# class Results:
