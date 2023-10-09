import csv
from initial import address_to_key, cleaned_distance_dict


class Package:
    def __init__(self, id, address: str, city: str, state: str, zip_code, delivery_deadline: str, weight, notes: str):
        self.id = int(id) if isinstance(id, str) else id
        self.address = address_to_key(address)
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = int(weight) if isinstance(weight, str) else weight
        self.notes = notes
        self.status = 'Undelivered'


def read_csv(file_path):
    # Replace list with hash function once completed
    packages = []
    with open(file_path) as file:
        reader = csv.reader(file)

        next(reader)
        for row in reader:
            package = Package(*row)
            packages.append(package)

    return packages


file_path = 'package_list.csv'
for package in read_csv(file_path):
    print(package.id)
    print(package.address)
    print(package.address in cleaned_distance_dict)
