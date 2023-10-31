import usaddress
from unclean_dict import unclean_dict


def time_to_value(time: str):
    hours, minutes = time.split(':')
    return int(hours) * 60 + int(minutes)


def address_to_key(address: str) -> str:
    # Parse the address using the `usaddress` library
    parsed_address, _ = usaddress.tag(address.strip())

    # Extract the address number and street name from the parsed address
    address_number = parsed_address.get('AddressNumber')
    street_name = parsed_address.get('StreetName')

    # Combine address number and street name to form a unique key
    key = f"{address_number} {street_name}".strip()

    return key


# Initialize an empty dictionary to store cleaned distances
cleaned_distance_dict = {}

# Iterate through unclean dictionary keys to clean them
for key in unclean_dict:
    new_key = address_to_key(key)

    temp_subdict = {}
    # Iterate through the subkeys in the unclean dictionary to clean them
    for subkey in unclean_dict[key]:
        new_subkey = address_to_key(subkey)
        # Update the temporary dictionary with the cleaned key and its associated value
        temp_subdict[new_subkey] = unclean_dict[key][subkey]

    # Update the cleaned distance dictionary with the cleaned key and its associated subdictionary
    cleaned_distance_dict[new_key] = temp_subdict
