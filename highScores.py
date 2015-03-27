import cPickle as pickle

class Score(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __gt__(self, other):
        return self.score > other.score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

def save(scorelist):
    with open("highscore.txt", "wb") as f:
        pickle.dump(scorelist, f)

def load():
    #sees if the list exists
    try:
        with open("highscore.txt", "rb") as f:
            scorelist = pickle.load(f)
        return scorelist
    #if not return an empty list
    except:
        scorelist = []
        for i in xrange(5):
            scorelist.append(Score("NAME", 0))
        return scorelist


