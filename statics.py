import json


def save_dict_to_json(data, filename):
    """
    Save dictionary in json file
    :param data: dictionary to save
    :param filename: filename to save it as
    :return: None
    """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def load_dict_from_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def interpret_days(days):

    if days == "MW":
        return 0, 2

    if days == "TT":
        return 1, 3

    if days == "WF":
        return 2, 4

    if days == "Mo":
        return 0, None

    if days == "Tu":
        return 1, None

    if days == "We":
        return 2, None

    if days == "Th":
        return 3, None

    if days == "Fr":
        return 4, None
