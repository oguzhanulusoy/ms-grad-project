class entity:

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


    def getName(self):
        return str(self.name)

    def getAttributes(self):
        return self.attributes

    def setName(self, name):
        self.name = str(name).lower()

    def setAttributes(self, attributes):
        if attributes != None:
            temp = []

            for item in self.attributes:
                temp.append(item)

            for item in attributes:
                temp.append(item)

            self.attributes = temp
        else:
            self.attributes = attributes

    def find(self, name):
        if self.name == str(name).lower():
            return self.attributes
