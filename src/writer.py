import numpy as np

class Writer:
    def __init__(self, vehicle_list, file_name):
        file = open(file_name, mode='w')
        text = ""

        for vehicle in vehicle_list:
            text += str(len(vehicle))
            for ride in vehicle:
                text += ' ' + str(ride)
            if vehicle != len(vehicle_list) - 1:
                text += '\n'

        file.write(text)
        file.close()