import usaddress
import ast
from unclean_dict import unclean_dict


def address_to_key(address: str) -> str:
    parsed_address, _ = usaddress.tag(address.strip())

    address_number = parsed_address.get('AddressNumber')
    street_name = parsed_address.get('StreetName')

    key = f"{address_number} {street_name}".strip()
    return key


cleaned_distance_dict = {}
for key in unclean_dict:
    new_key = address_to_key(key)

    temp_subdict = {}
    for subkey in unclean_dict[key]:
        new_subkey = address_to_key(subkey)
        temp_subdict[new_subkey] = unclean_dict[key][subkey]

    cleaned_distance_dict[new_key] = temp_subdict
