from json import JSONEncoder
import emote_list


class EListEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, emote_list.EmoteList):
            return o.get_totals().__dict__
