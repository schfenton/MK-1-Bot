

class Poll:
    """Class representing a poll with the ability to add """

    def __init__(self, **kwargs):

        self.candidates = []
        self.votes = []
        self.open = False
        self.result = None

    def add_candidate(self, candidate):


    def remove_candidate(self, candidate):


    def open_poll(self):
        self.open = True

    def add_score(self, key, value):


    def remove_score(self, key, value):
