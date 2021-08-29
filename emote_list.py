import re


# Utility Functions
def parse_message(msg):
    """ Returns array of emote ids within a message, or an empty array if no emotes are found """
    return re.findall(r"<:\w+:\d+>", msg)


class EmoteList:
    """Implements a data structure to store total frequency of emotes as well as frequencies of emoji for each user
        using Python dictionaries. The frequency of individual emotes is handled in this class whereas frequency of
        emotes per user is handled in the UserDict class."""

    def __init__(self):
        self.totals = {}
        # self.users = UserMap()

    def get_totals(self):
        """Returns the dictionary containing all emote ids and the frequency they were used across the server"""
        return self.totals

    def add(self, emote_id, user):
        """Increases use count of an emoji by one in both the total and for the message author"""
        # add 1 to freq of emote_id, or initialize if key does not exist
        if emote_id in self.totals:
            self.totals[emote_id] += 1
        else:
            self.totals[emote_id] = 1

        # add to user emote frequency
        # self.users.add(user, emote_id)

    # def sub(self, emote_id, user):

    # def del_emote(self, emote_id):

    # def del_user(self, user):


class UserMap:
    """Subclass to track how many times a user uses each emote using a nested dictionary, with the first dictionary
    containing the user as the key and the inner dictionary containing how many times that user used each emote."""

    def __init__(self):
        self.user_freq = {}

    def add(self, user, emote):
        """Adds one to the use count with respect to the user, and initializes the value if the user exists and the
        emote doesn't or if the user doesn't exist"""
        if user in self.user_freq:
            if emote in self.user_freq[user]:
                self.user_freq[user][emote] += 1
            else:
                self.user_freq[user][emote] = 1
        else:
            self.user_freq[user] = {emote: 1}
        return None

    # def sub(self, user, emote):
    #     return None

    def get_user_emote_frequency(self, user):
        """Returns the emote frequency dictionary of the user passed in the argument"""
        if user in self.user_freq:
            return self.user_freq[user]
        else:
            return None

    # def get_all_emote_frequency(self, user):
    #     freq = {}
    #     for user, ufreqs in self.user_freq.items():

    # def del_user(self, user):
    #     """"""
    #
    # def del_emote(self, emote):
