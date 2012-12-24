import uuid

class WordsmushPlayer(object):
    
    def __init__(self, name=None):
        self.name = name or uuid.uuid4() 
        self.score = 0

