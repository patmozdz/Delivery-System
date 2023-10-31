# Student ID: 011247440
from unclean_dict import unclean_dict
from classes import Package, Truck
from helpers import time_to_value


def ui_loop():
    intro_message = """
    Welcome to the WGUPS Package Delivery System!
    Please enter 's' to view the status of all packages at a specific time,
    Enter "q" to quit,
    Enter "h" to view this message again.
    """

    print(intro_message)
    while True:
        user_input = input('Enter menu option: ')
        if user_input == 's':
            start_time = input("Please enter the start time in HH:MM format: ")
            start_time = time_to_value(start_time)

            end_time = input("Please enter the end time in HH:MM format: ")
            end_time = time_to_value(end_time)

            nodes = [node for node in Package.current_day_packages if node.data is not None]
            packages = []
            for node in nodes:
                while node:
                    packages.append(node.data)
                    node = node.next

            packages_in_timeframe = []
            all_other_packages = []
            for package in packages:
                if package.status.split()[0] == 'Delivered' and start_time <= time_to_value(package.status.split()[-1]) <= end_time:
                    packages_in_timeframe.append(package)
                else:
                    all_other_packages.append(package)

            print("\n\tPackages delivered in the specified timeframe:\n")
            for package in packages_in_timeframe:
                print(f'Package with id: {package.id} was delivered at {package.status.split()[-1]}')

        elif user_input == 'q':
            break
        elif user_input == 'h':
            print(intro_message)
        else:
            print("Invalid input. Please try again.")


def main():
    # Set the current day's packages from the CSV file
    Package.set_current_day_packages('package_list.csv')

    # Initialize two trucks with unique IDs
    truck1 = Truck(1, '09:05')
    truck2 = Truck(2, '08:00')

    # Priority packages for truck2 categorized by their level of priority
    truck2_top_priority = [15]
    truck2_mid_priority = [13, 14, 16, 20, 40]
    truck2_no_priority = [19, 38, 3, 18, 36]

    # Priority packages for truck1 categorized by their level of priority
    truck1_top_priority = [6, 25, 29, 30, 31, 34, 37]
    truck1_no_priority = [28, 32, 9]

    # Remaining packages that haven't been prioritized yet
    remainder = [35, 12, 24, 22, 21, 39, 33, 7, 23, 11, 1, 2, 27, 10, 26, 5, 8, 17, 4]

    # Load prioritized and non-prioritized packages onto truck1 and truck2
    truck1.load(remainder, truck1_top_priority, truck1_no_priority)
    truck2.load(remainder, truck2_top_priority, truck2_mid_priority, truck2_no_priority)

    # Drive both trucks, with truck1 returning to the hub after delivering
    truck1.drive(go_back=True)
    truck2.drive()

    # Load the remaining packages onto truck1 and drive again
    truck1.load(remainder)
    truck1.drive()

    # Print the total distance traveled by both trucks
    print(f'Total distance traveled: {(truck1.total_dist_traveled + truck2.total_dist_traveled):.2f} miles')

    # Run the user interface loop
    ui_loop()


# Call the main function
main()
