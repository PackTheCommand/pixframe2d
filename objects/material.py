class Material:
    def __init__(self, map):
        self.map = map
        self.top = map["n"]
        self.bottom = map["s"]
        self.left = map["w"]
        self.right = map["e"]
        self.nw = map["nw"]
        self.ne = map["ne"]
        self.sw = map["sw"]
        self.uniquename = map["uniqueName"]
        self.se = map["se"]

    def getUNIQE(self):
        return self.uniquename
