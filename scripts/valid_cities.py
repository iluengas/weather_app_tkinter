
def add_valid_city(city_name):
    """
    Adds a valid city to the list of valid cities stored in the 'valid_cities.txt' file.

    Args:
        city_name (str): Name of the city to add.

    Returns:
        None
    """
    cities = []
    with open("scripts/valid_cities.txt", 'r') as reading:
        for line in reading:
            cities.append(line.strip().lower())

    if city_name.lower() not in cities:
        print("Adding:", city_name, "to the valid cities file")
        with open("scripts/valid_cities.txt", 'a') as appending:
            appending.write(city_name)
            appending.write("\n")


def get_valid_cities():
    """
    Returns a list of valid cities stored in the 'valid_cities.txt' file.

    Returns:
        list: A list of valid cities.
    """
    with open("scripts/valid_cities.txt", 'r') as reading:
        cities = [line.strip() for line in reading]

    return cities
