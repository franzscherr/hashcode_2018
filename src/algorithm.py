import numpy as np


def dist(src, dest):
    return np.abs(src[0] - dest[0]) + np.abs(src[1] - dest[1])


class GreedyAlgorithm(object):
    def __init__(self, rides, meta):
        self.rides = rides
        self.meta = meta
        self.vehicles = list()
        for i in range(meta.F):
            self.vehicles.append(list())

    def nearest_ride(self, open_rides, src, timestep):
        shortest_ride = open_rides.pop()
        open_rides.add(shortest_ride)
        shortest_ride_distance = np.inf
        for ride in open_rides:
            d = dist(src, (ride.a, ride.b))
            if timestep + d < ride.s:
                d = ride.s
            if d < shortest_ride_distance:
                shortest_ride_distance = d
                shortest_ride = ride
        return shortest_ride

    def assign_rides(self):
        current_vehicle_timestep = np.zeros(self.meta.F)
        current_vehicle_position = list()
        for _ in range(self.meta.F):
            current_vehicle_position.append((0, 0))
        open_rides = set(self.rides)
        n_open_rides = len(self.rides)

        while n_open_rides > 0:
            vehicle_ind = np.argmin(current_vehicle_timestep)

            ride_found = False
            while not ride_found and n_open_rides > 0:
                nearest_ride = self.nearest_ride(open_rides,
                                                 current_vehicle_position[vehicle_ind],
                                                 current_vehicle_timestep[vehicle_ind])
                if nearest_ride.latest_start < current_vehicle_timestep[vehicle_ind]:
                    ride_found = True
                    open_rides.remove(nearest_ride)

