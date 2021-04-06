import datetime

class sentence:

    def __init__(self, subject, verb, object, multiplicities, primaryKeys):
        self.id = str(datetime.datetime.now())
        self.subject = subject[0]
        self.verb = verb
        self.object = object
        self.multiplicities = multiplicities
        self.primaryKeys = primaryKeys

    def get_id(self):
        return str(self.id)

    def getSubject(self):
        return str(self.subject)

    def setSubject(self, subject):
        try:
            if self.getSubject():
                already_added = self.getSubject()
                recently_added = str(subject).lower()
                self.subject = already_added + ',' + recently_added
            else:
                self.subject = str(subject).lower()
        except:
            print()

    def getVerb(self):
        return str(self.verb)

    def setVerb(self, verb):
        try:
            if self.getVerb():
                already_added = self.getVerb()
                recently_added = str(verb).lower()
                self.verb = already_added + ',' + recently_added
            else:
                self.verb = str(verb).lower()
        except:
            print()

    def getObject(self):
        return self.object

    def setObject(self, object):
        try:
            if self.getObject():
                already_added = self.getObject()
                recently_added = str(object).lower()
                self.object = already_added + ',' + recently_added
            else:
                self.object = str(object).lower()
        except:
            print()

    def getSentence(self):
        return "{} {} {}".format(self.getSubject(), self.getVerb(), self.getObject())

    def getPrimaryKeys(self):
        return self.primaryKeys

    def getMultiplicities(self):
        return self.multiplicities
