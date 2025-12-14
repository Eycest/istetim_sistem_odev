class Surec:
    def __init__(self, id, g, s, o):
        self.id = id
        self.g = g
        self.s = s
        self.k = s
        self.o = o

    def sozluk(self):
        return {"id": self.id, "g": self.g, "s": self.s, "k": self.k, "o": self.o}
