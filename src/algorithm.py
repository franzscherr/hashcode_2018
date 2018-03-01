import numpy as np


def dist(src, dest):
    return np.abs(src[0] - dest[0]) + np.abs(src[1] - dest[1])


def spacetime_dist(vehicle_pos, vehicle_timestep, ride):
    d = dist(vehicle_pos, (ride.a, ride.b))
    if vehicle_timestep + d >= ride.latest_start:
        d = np.inf
    d = np.max([d, ride.s - vehicle_timestep])
    return d


class MCTSAlgorithm(object):
    def __init__(self, rides, meta):
        self.rides = list(sorted(rides, key=lambda a: getattr(a, 's')))
        self.meta = meta
        self.vehicles = list()
        self.assigned_rides = list()
        for i in range(meta.F):
            self.vehicles.append(list())
            self.assigned_rides.append(list())
        self.depth = 2

    def assign_rides(self):
        current_vehicle_timestep = np.zeros(self.meta.F)
        current_vehicle_position = list()
        for _ in range(self.meta.F):
            current_vehicle_position.append((0, 0))

        depth = 10
        n_samples = 10

        n_rides = len(self.rides)
        import tqdm
        t_range = tqdm.tqdm(range(n_rides - 1))
        for i in t_range:
            root_node = dict()
            for j in range(self.meta.F):
                root_node[j] = []
            for i_sample in range(n_samples):
                sample_current_timestep = np.copy(current_vehicle_timestep)
                sample_current_position = []
                for vec_id in range(self.meta.F):
                    sample_current_position.append(current_vehicle_position[vec_id])

                reward = 0
                first_ride_vehicle = None
                for i_tree in range(np.min([depth, n_rides - i])):
                    ride = self.rides[i + i_tree]
                    dists = []
                    for j in range(self.meta.F):
                        d = spacetime_dist(current_vehicle_position[j], current_vehicle_timestep[j], ride)
                        dists.append(d)
                    dists = np.array(dists)
                    if np.all(np.isinf(dists)):
                        continue

                    vehicle_indices = np.arange(self.meta.F)
                    p = np.exp(-(dists - np.min(dists)) / (np.max(dists) - np.min(dists)))
                    p[np.isinf(dists)] = 0
                    vehicle_ind = np.random.choice(vehicle_indices, p=p)
                    if i_tree == 0:
                        first_ride_vehicle = vehicle_ind
                    reward += ride.d
                    sample_current_timestep[vehicle_ind] += np.min(dists) + ride.d
                    sample_current_position[vehicle_ind] = (ride.x, ride.y)
                if first_ride_vehicle is not None:
                    root_node[first_ride_vehicle].append(reward / (np.max(sample_current_timestep) - \
                                                                   current_vehicle_timestep[first_ride_vehicle]))
            means = np.zeros(self.meta.F)
            for k, v in root_node.items():
                means[k] = np.mean(v)
            self.assigned_rides[np.argmax(means)].append(self.rides[i].id)


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
                d = ride.s - timestep
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
            print(n_open_rides)
            if len(skip_vehicles) > 0:
                modified_vehicle_timestep = np.copy(current_vehicle_timestep)
                modified_vehicle_timestep = modified_vehicle_timestep.astype(dtype=np.float64)
                for vehicle_ind in skip_vehicles:
                    modified_vehicle_timestep[vehicle_ind] = np.inf
                vehicle_ind = np.argmin(modified_vehicle_timestep)
            else:
                vehicle_ind = np.argmin(current_vehicle_timestep)

            ride_found = False
            while not ride_found and n_open_rides > 0:
                nearest_ride, spacetime_dist = self.nearest_ride(open_rides,
                                                                 current_vehicle_position[vehicle_ind],
                                                                 current_vehicle_timestep[vehicle_ind])
                if nearest_ride.latest_start > current_vehicle_timestep[vehicle_ind] + \
                        dist(current_vehicle_position[vehicle_ind], (nearest_ride.a, nearest_ride.b)):
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
                        break

            if ride_found:
                current_vehicle_position[vehicle_ind] = (nearest_ride.x, nearest_ride.y)
                current_vehicle_timestep[vehicle_ind] = current_vehicle_timestep[vehicle_ind] + \
                                                        spacetime_dist + nearest_ride.d
                self.assigned_rides[vehicle_ind].append(nearest_ride.id)
                skip_vehicles.clear()
