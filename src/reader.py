import numpy as np
from meta_info import MetaInfo
from ride import Ride


class Reader:
    def __init__(self, file_name):
        file = open(file_name, mode='r')
        lines = file.read().split('\n')
        file.close()

        info = map(int, lines[0].split(' '))
        R, C, F, N, B, T = info;
        self.meta_info = MetaInfo(R, C, F, N, B, T)
        self.rides = []

        for id in range(len(lines) - 2):
            line_index = id + 1
            info = map(int, lines[line_index].split(' '))
            a, b, x, y, s, f = info;
            ride = Ride(a, b, x, y, s, f, id)
            self.rides.append(ride)

    def get_meta_info(self):
        return self.meta_info

    def get_rides(self):
        return self.rides





