import csv
import usaddress
from collections import deque
from itertools import permutations
from clean_distance_dict import cleaned_distance_dict


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Package:
    current_day_packages = [Node(None)] * 40

    def __init__(self, id, address: str, city: str, state: str, zip_code, delivery_deadline: str, weight, notes: str, required_truck=None):
        self.id = int(id) if isinstance(id, str) else id
        self.address = self.address_to_key(address)
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = int(weight) if isinstance(weight, str) else weight
        self.notes = notes
        self.status = 'Waiting at Hub'
        self.required_truck = required_truck

    @classmethod
    def hash_lookup(cls, id):
        index = (id - 1) % len(cls.current_day_packages)
        node = cls.current_day_packages[index]

        # Traverse through linked list to account for collisions
        while node:
            if node.data and node.data.id == id:
                return node.data
            else:
                node = node.next

    @classmethod
    def hash_insert(cls, package):
        index = (package.id - 1) % len(cls.current_day_packages)

        if cls.current_day_packages[index].data is None:
            cls.current_day_packages[index] = Node(package)
        else:  # Collision
            cls.current_day_packages[index].next = Node(package)

    @staticmethod
    def csv_to_package_objects(file_path):
        with open(file_path) as file:
            # Initialise list of packages so that items can be inserted in any order
            reader = csv.reader(file)
            row_count = sum(1 for row in reader)
            packages = [0] * (row_count - 1)  # Subtract 1 to account for header row

            file.seek(0)
            next(reader)
            for row in reader:
                package = Package(*row)
                packages[package.id - 1] = package

        return packages

    @staticmethod
    def set_current_day_packages(file_path):
        for package in Package.csv_to_package_objects(file_path):
            Package.hash_insert(package)            


class Truck:
    max_capacity = 16
    HUB = Package.address_to_key("Western Governors University 4001 South 700 East, Salt Lake City, UT 84107")

    def __init__(self, id):
        self.id = id
        self.package_groups = deque()
        self.current_location = self.HUB
        self. total_dist_traveled = 0

    def load(self, remainder, *args: list):  # Modify this function to be "smart search" so that it loads packages that have addresses already in the truck first
        assert self.current_location == self.HUB
        for arg in args:
            assert isinstance(arg, list)
            self.package_groups.append(arg)

        to_fill = self.get_empty_spots()
        if to_fill == self.max_capacity:
            self.package_groups.append([])

        if to_fill > len(remainder):
            self.package_groups[-1].extend(remainder)
            del remainder[:]

        else:
            self.package_groups[-1].extend(remainder[-to_fill:])
            del remainder[-to_fill:]

    def drive(self, go_back=False):
        for current_group in self.package_groups:
            for package_id in current_group:
                # CHANGE TO HASH FUNCTION ONCE MADE
                package = Package.hash_lookup(package_id)
                package.status = 'In Transit'

        while self.package_groups:
            current_group = self.package_groups.popleft()
            route, route_dist = self.calculate_best_combination(current_group, go_back=go_back)
            self.total_dist_traveled += route_dist
            self.current_location = route[-1]

            for location in route:
                for package_id in current_group:
                    package = Package.hash_lookup(package_id)

                    if package.address == location:
                        package.status = 'Delivered'
                        current_group.remove(package.id)

                for other_group in self.package_groups:
                    for package_id in current_group:
                        package = Package.hash_lookup(package_id)

                        if package.address == location:
                            package.status = 'Delivered'
                            other_group.remove(package)

    def calculate_best_combination(self, package_group, go_back=False):
        start_position = self.current_location
        all_permutations = permutations(package_group)

        first_permutation = next(all_permutations)
        first_permutation_locations = tuple(Package.hash_lookup(package_id).address for package_id in first_permutation)
        best_route = (start_position,) + first_permutation_locations
        best_route_total_dist = self.route_total_dist(best_route)
        if not self.package_groups and go_back is True:
            best_route = best_route + (self.HUB,)

        for permutation in all_permutations:
            permutation_locations = tuple(Package.hash_lookup(package_id).address for package_id in permutation)
            route = (start_position,) + permutation_locations

            if not self.package_groups and go_back is True:
                route = route + (self.HUB,)

            if (total_dist := self.route_total_dist(route)) < best_route_total_dist:
                best_route = route
                best_route_total_dist = total_dist

        return best_route, best_route_total_dist

    def distance_between(self, city1, city2):
        return cleaned_distance_dict[city1][city2]

    def route_total_dist(self, route):
        total_dist = 0
        for i in range(len(route) - 1):
            total_dist += self.distance_between(route[i], route[i + 1])

        return total_dist

    def get_empty_spots(self):
        if not self.package_groups:
            return self.max_capacity
        else:
            filled_spots = sum(len(package_group) for package_group in self.package_groups)

            return self.max_capacity - filled_spots
