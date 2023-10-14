# Student ID: 011247440
from unclean_dict import unclean_dict
from classes import Package, Truck


def main():
    Package.set_current_day_packages('package_list.csv')

    truck1 = Truck(1)
    truck2 = Truck(2)

    truck2_top_priority = [15]
    truck2_mid_priority = [13, 14, 16, 20, 40]
    truck2_no_priority = [19, 38, 3, 18, 36]

    truck1_top_priority = [6, 25, 29, 30, 31, 34, 37]
    truck1_no_priority = [28, 32, 9]

    remainder = [35, 12, 24, 22, 21, 39, 33, 7, 23, 11, 1, 2, 27, 10, 26, 5, 8, 17, 4]

    truck1.load(remainder, truck1_top_priority, truck1_no_priority)
    truck2.load(remainder, truck2_top_priority, truck2_mid_priority, truck2_no_priority)

    truck1.drive(go_back=True)
    truck2.drive()

    truck1.load(remainder)
    truck1.drive()

    print(truck1.total_dist_traveled + truck2.total_dist_traveled)


main()
