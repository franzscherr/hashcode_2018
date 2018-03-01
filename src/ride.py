import numpy as np

class Ride:
    def __init__(self, a, b, x, y, s, f, id):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s
        self.f = f
        self.d = np.abs(a-x)+np.abs(b-y)
        self.latest_start = self.f - self.d
