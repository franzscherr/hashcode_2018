import numpy as np

class Reader:
    def __init__(self, file_name):
        file = open(file_name, mode='r')
        lines = file.read().split('\n')
        file.close()

        self.data = None

    def get_data(self):
        return self.data





