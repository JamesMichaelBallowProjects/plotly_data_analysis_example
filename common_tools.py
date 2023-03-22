# MODULES
# --- others' modules
import uuid
import os
from datetime import datetime
import pandas as pd
import numpy as np


class Logger:
    def __init__(self, logFile):
        self.logFile = logFile
        self.__generate_log_file()
        self.__log_datetime()

    def __log_datetime(self):
        sep = "-" * 80
        sep2 = "-" * 49
        self.log(sep + '\n')
        self.log(sep + '\n')
        self.log("-----" + str(datetime.now()) + sep2 + '\n')
        self.log(sep + '\n')
        self.log(sep + '\n')

    def __generate_log_file(self):
        if not os.path.isfile(self.logFile):
            open(self.logFile, 'w').close()

    def log(self, details):
        with open(self.logFile, 'a') as f:
            f.write(details)


class Colour:
    """ Color codes for string printing in different colors.
        Used the Old English 'Colour' to separate from other common packages.
    """
    # methods for concatenating string with color codes
    def red(string):
        return "\033[31m" + str(string) + "\033[37m"

    def yellow(string):
        return "\033[33m" + str(string) + "\033[37m"

    def green(string):
        return "\033[32m" + str(string) + "\033[37m"

    def blue(string):
        return "\033[34m" + str(string) + "\033[37m"

    def purple(string):
        return "\033[35m" + str(string) + "\033[37m"

    def white(string):
        return "\033[37m" + str(string)


def sort_json_keys(json_obj):
    """Sort [a->z] the immediately accessible set of keys.

    Args:
        json_obj (dict): object to be sorted at top-most level.

    Returns:
        dict: same as json_obj but sorted top-most level keys [a->z].
    """
    tmp = {}
    for key in sorted(json_obj.keys()):
        tmp[key] = json_obj[key]
    return tmp


def dollar_variable_replacement(template, dVars):
    """Find '$@' in a text and replace with another string.
    Term "dVars" is short for "dollar variables", which are
    the terms that are prepended with '$@'.

    Args:
        template (str): any string with optional '$@' vars.
        dollarVariables (dict): replacement keys and values.

    Returns:
        str: [template] input with all '$@' replaced.
    """
    assert (type(template) == str)
    assert (type(dVars) == dict)
    newString = template
    for key in dVars.keys():
        newString = newString.replace("$@" + str(key), str(dVars[key]))
    return newString


# files
def open_file_read_contents(file_path):
    """Opens a file with read permissions and reads all contents into a string.

    Args:
        file_path (_type_): absolute or relative path to a file to be opened.

    Raises:
        Exception: failure to open/read file (permissions or file existence).

    Returns:
        str: string of all contents from file.
    """
    try:
        with open(file_path, "r") as f:
            contents = f.read()
    except Exception:
        raise Exception("Issue with reading" + file_path + "."
                        "Check if exists and permissions.")
    return contents


def read_csv_into_memory(file):
    """Opens csv file from a relative or full path.

    Args:
        file (str): relative or full path to csv file to be opened.

    Raises:
        FileNotFoundError: If file path does not exist.

    Returns:
        pd.DataFrame: data inside of csv file.
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(
            "Attempted (and failed) to read" + file +
            "into memory; file is missing at provided path.")
    return pd.read_csv(file)


# identifications
def get_uid():
    """Generate UID using uuid4 - only first sect of digits is kept."""
    uid_full = str(uuid.uuid4())
    return uid_full.split("-")[0]


# indicies
def find_all_indices_of_item(list_to_check: list,
                             item_to_find) -> list:
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices


def get_index_closest_matching_intvalue(listOfValues, searchValue):
    """Get index of a item in list closest to provided reference value.

    Args:
        listOfValues (list[int]): any list of int values in which to search.
        searchValue (int): value to look for in list.

    Returns:
        int: index of closest matching value.
    """
    diff = [(x - searchValue)**2 for x in listOfValues]
    return diff.index(min(diff))


def filter_values_between_limits(y,
                                 lowerLimit: float,
                                 upperLimit: float = None,
                                 ) -> dict:
    # grab peaks above lower limit
    aboveLower = [n > lowerLimit for n in y]

    # grab peaks belower upper limit
    if upperLimit is not None:
        belowUpper = [n < upperLimit for n in y]
    else:
        belowUpper = [True] * len(aboveLower)

    # combine limit filters
    bothLimitsBool = [a and b for a, b in zip(belowUpper, aboveLower)]
    bothLimitsMag = np.array(y) * bothLimitsBool
    return bothLimitsBool, bothLimitsMag


def filter_top_N_values(y,
                        N: int = 1
                        ) -> dict:
    topN_idx = []
    topN_val = []
    nElem = len(y)
    if nElem <= N:
        return np.arange(0, nElem), y, y

    newY = np.zeros(shape=(nElem,), dtype=float)
    setY = list(set(y))
    setY.sort(reverse=True)
    for d in setY:
        i = find_all_indices_of_item(list_to_check=y, item_to_find=d)
        for idx in i:
            topN_idx.append(idx)
            topN_val.append(y[idx])
    topN_idx = topN_idx[:N]
    topN_val = topN_val[:N]
    for n in topN_idx:
        newY[n] = y[n]
    return topN_idx, topN_val, newY


def get_ranges_from_binary_list(nums):
    """Get the start and stop ranges in a list of ints
    that correlate to the ranges of non-zero elements.

    Example: [0,0,0,4,1,0,67,0] will return [[3,5],[6,7]]

    Args:
        nums (list[int]): mixture of contiguous and non-contiguous ints.

    Returns:
        list[list[int]]: ranges ([start,stop]) of contiguous non-zero ints.
    """
    ranges = []
    startEnabled = False
    for i, n in enumerate(nums):
        if n:
            if not startEnabled:
                start = i
                startEnabled = True
            if i == len(nums)-1:
                ranges.append([start, i])
        else:
            if startEnabled:
                ranges.append([start, i])
            startEnabled = False
    return ranges


# data conversionts
def time_in_seconds(number: float,
                    currentUnit: str) -> float:
    if currentUnit == 'years':
        s = 31556926
    elif currentUnit == 'months':
        s = 2629743.83
    elif currentUnit == 'weeks':
        s = 604800
    elif currentUnit == 'days':
        s = 86400
    elif currentUnit == 'hours':
        s = 3600
    elif currentUnit == 'minutes':
        s = 60
    elif currentUnit == 'seconds':
        s = 1
    else:
        raise Exception(f"Cannot convert {currentUnit} "
                        "to seconds (not programmed).")
    s *= number
    return s
