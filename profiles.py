import json

class Relation(object):
    def __init__(self, name, gender, id):
        self.name = name
        self.id = id
        self.gender = gender

class Profile(object):
    relations = []
    def __init__(self, id, geniLink, name, relations, gender):
        self.id = id
        self.name = name
        self.geniLink = geniLink
        self.relations = relations
        self.gender = gender
    def addRelation(self, name, gender, id):
        r = Relation(name, gender, id)
        self.relations.append(r)
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
