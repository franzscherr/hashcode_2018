import numpy as np


def dist(src, dest):
    return np.abs(src[0] - dest[0]) + np.abs(src[1] - dest[1])


class GreedyAlgorithm(object):
    def __init__(self, rides, meta):
        self.rides = rides
        self.meta = meta
        self.vehicles = list()
        self.assigned_rides = list()
        for i in range(meta.F):
            self.vehicles.append(list())
            self.assigned_rides.append(list())

    def nearest_ride(self, open_rides, src, timestep):
        shortest_ride_distance = np.inf
        for ride in open_rides:
            d = dist(src, (ride.a, ride.b))
            if timestep + d < ride.s:
                d = ride.s
            if d < shortest_ride_distance:
                shortest_ride_distance = d
                shortest_ride = ride
        return shortest_ride, shortest_ride_distance

    def assign_rides(self):
        current_vehicle_timestep = np.zeros(self.meta.F)
        current_vehicle_position = list()
        for _ in range(self.meta.F):
            current_vehicle_position.append((0, 0))
        open_rides = set(self.rides)
        n_open_rides = len(self.rides)
        skip_vehicles = list()

        while n_open_rides > 0:
            if len(skip_vehicles) > 0:
                modified_vehicle_timestep = np.copy(current_vehicle_timestep)
                modified_vehicle_timestep = modified_vehicle_timestep.astype(dtype=np.float64)
                for vehicle_ind in skip_vehicles:
                    modified_vehicle_timestep[vehicle_ind] = np.inf
                vehicle_ind = np.argmin(modified_vehicle_timestep)
                skip_vehicles.clear()
            else:
                vehicle_ind = np.argmin(current_vehicle_timestep)

            ride_found = False
            while not ride_found and n_open_rides > 0:
                nearest_ride, spacetime_dist = self.nearest_ride(open_rides,
                                                                 current_vehicle_position[vehicle_ind],
                                                                 current_vehicle_timestep[vehicle_ind])
                if nearest_ride.latest_start > current_vehicle_timestep[vehicle_ind] + spacetime_dist:
                    ride_found = True
                    open_rides.remove(nearest_ride)
                    n_open_rides -= 1
                else:
                    # ______________________________________________________________________________
                    # CHECK IF ANY VEHICLE CAN MAKE THIS RIDE
                    cannot_fulfill = True
                    for i in range(self.meta.F):
                        d = dist(current_vehicle_position[i], (nearest_ride.a, nearest_ride.b))
                        if current_vehicle_timestep[i] + d < nearest_ride.latest_start:
                            cannot_fulfill = False
                            break
                    if cannot_fulfill:
                        open_rides.remove(nearest_ride)
                        n_open_rides -= 1
                    else:
                        skip_vehicles.append(vehicle_ind)

            if ride_found:
                current_vehicle_position[vehicle_ind] = (nearest_ride.x, nearest_ride.y)
                current_vehicle_timestep[vehicle_ind] = current_vehicle_timestep[vehicle_ind] + \
                                                        spacetime_dist + nearest_ride.d
                self.assigned_rides[vehicle_ind].append(nearest_ride.id)
