##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2020, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
almutils.py
Various utilities that can be used by other parts of ALAMOpy.
"""
import os
import subprocess
import numpy as np

from alamopy import exec_path


def datadim(arr):
    """
    Determine the number of dimensions involved in data from a given 2D array.
    Args:
        arr: a 2D list representing a series of data points, each data point
            represented by a 1D list element.
    Returns:
        The number of dimensions that the data points in the array represent.
    Example: [[1], [2], [3]] -> 1
    Example: [[1,2,3], [4,5,6], [7,8,9], [10,11,12]] -> 3
    """
    return len(arr[0])


def arr2str(arr):
    """
    Prepare a space-delimited string representation of the input array.
    Args:
        arr: a singleton or 1D or 2D array-like data structure.
    Returns:
        A string representation of arr suitable to be printed to an alm file.
    Example: 2 -> "2"
    Example: [2, 3, 4] -> "2 3 4"
    Example: [[1, 2], [3, 4], [5, 6]] -> "1 2\n3 4\n5 6"
    """
    dim = np.asarray(arr).ndim

    # 0D singleton
    if dim == 0:
        return str(arr)

    # 1D array
    if dim == 1:
        target_list = []
        for item in arr:
            target_list.append(" ")
            target_list.append(str(item))
        return "".join(target_list[1:])

    # 2D array
    target_list = []
    for sublist in arr:
        target_list.append("\n")
        target_list.append(arr2str(sublist))
    return "".join(target_list[1:])


def alm2lst(alm_file_name):
    """
    Return a suitable .lst file name based on the input .alm file name.
    Args:
        alm_file_name: name (including full directory and extension) of the
            .alm file that will be written by ALAMOpy.
    Returns:
        A name at which the .lst file generated by the ALAMO executable can be
            found. If the input alm file name doesn't have any extension, the
            lst name will be generated by inserting a .lst extension to the alm
            name. If the input alm file name has any extension, the lst name
            will be generated by changing its extension to .lst.
    Example: "~/temp" -> "~/temp.lst"
    Example: "~/.temp.alm" -> "~/.temp.lst"
    """
    return os.path.splitext(alm_file_name)[0] + ".lst"


def zip_2d_lists(list_a, list_b):
    """
    Provide a zipped list view of the given two 2D lists.
    Args:
        list_a: a 2D list
        list_b: another 2D list
    Returns:
        A zipped list, each element of which is a concatenation of the
            corresponding two elements from list_a and list_b.
    Example:
        a = [[1], [2], [3]]
        b = [[4], [5], [6]]
        almutils.ziplists(a, b) = [[1, 4], [2, 5], [3, 6]]
    """
    return [a_elem + b_elem for a_elem, b_elem in zip(list_a, list_b)]


def represent_model_str(term_list):
    """
    Given a list of terms represented in ALAMO's format, return a string that
    represents the same model in ordinary mathematical format.
    Args:
        term_list: a list of strings, each string containing a term. Such a
            term would contain some variables separated by spaces, meaning that
            these variables are to be timed together.
    Returns:
        A single list in the format of "a +/- b +/- c", where a, b, and c are
            terms in the argument term_list. If the list is empty, represent 0.
    Example:
        ["1.0 X1", "0.5 X2"] -> "1.0 * X1 + 0.5 * X2"
        ["1.0 X1", "-0.5 X2^3"] -> "1.0 * X1 - 0.5 * X2^3"
        [] -> "0"
    """
    if term_list == []:
        return "0"

    target = []
    for item in term_list:
        item_target = []
        for variable in item.split():
            item_target.append(" * ")
            item_target.append(str(cast(variable)))
        item_str = "".join(item_target[1:])
        if item_str[0] == "-":
            target.append(" - ")
            item_str = item_str[1:]
        else:
            target.append(" + ")
        target.append(item_str)
    if target[0] == " + ":
        target = target[1:]
    return "".join(target)


def data2min(data):
    """
    Given a 2D array, return a 1D array with length equal to that of an element
    of the 2D array. Each field in the returned 1D array will be equal to the
    minimum on that corresponding dimension across all data points in the
    original 2D array.
    Args:
        data: a rectangular 2D array.
    Returns:
        A 1D numpy ndarray containing the minimum on each dimension.
    Example:
        [[0,1],[2,-1]] -> [0,-1]
    """
    res = data[0]
    for item in data:
        res = np.minimum(res, item)
    return res


def data2max(data):
    """
    Given a 2D array, return a 1D array with length equal to that of an element
    of the 2D array. Each field in the returned 1D array will be equal to the
    maximum on that corresponding dimension across all data points in the
    original 2D array.
    Args:
        data: a rectangular 2D array.
    Returns:
        A 1D numpy ndarray containing the maximum on each dimension.
    Example:
        [[0,1],[2,-1]] -> [2,1]
    """
    res = data[0]
    for item in data:
        res = np.maximum(res, item)
    return res


def only_contains(line, char):
    """
    Returns true iff this given non-empty string only contains the given char.
    Args:
        line: a string
        char: a character
    Returns:
        True iff the string is not empty and it only contains the given char.
    Example:
        ("*****", '*') -> True
        ("", '*') -> False
    """
    line_len = len(line)
    if line_len == 0:
        return False
    for i in range(line_len):
        curr_char = line[i]
        if curr_char != char:
            return False
    return True


def nets(items, i, func):
    """
    nets stands for Next Element That Satisfies.
    Returns (j, item) such that item == items[j] and that item is the next
    element from the given list (counting starting from items[i], inclusive)
    that satisfies f. If no element in the list starting at index i satisfies
    f, returns None.
    Args:
        items: a list
        i: the index that counting starts at
        f: a function that can take in an item from the list and return a
            boolean value.
    Returns:
        (j, item) such that item == items[j] and that item is the next element
        from the given list items (counting starts from items[i], inclusive)
        that satisfies f. None if no element in items starting at index i
        satisfies f.
    Example:
        ([1, 2, 3], 0, lambda x: x % 2 != 0) -> (0, 1)
        ([1, 2, 3], 0, lambda x: x < 0) -> None
    """
    try:
        return next((ind + i, ele) for ind, ele in enumerate(items[i:]) if func(ele))
    except StopIteration:
        return None


def cast(var):
    """
    If var is a string representation of an int/float number, return that
    number. If var is 'T', return True. If var is 'F', return False. Else,
    return var itself without casting.
    Args:
        var: any variable
    Returns:
        An int equal to var, if car is an int representation.
        A float equal to var, if var is a float representation.
        A bool equal to True/False if var is "T" or "F".
        Else, just var itself.
    Example:
        '1e4' -> 10000
        '3.0' -> 3.0
        'T' -> True
        't' -> 't'
    """
    try:
        return int(var)
    except ValueError:
        try:
            return float(var)
        except ValueError:
            if var == "T":
                return True
            if var == "F":
                return False
            return var


def increment(item_list, index, num_steps):
    """
    Return the (index, element) pair after taking num_steps steps forward from
    the given index. If there is no more element in the list, return None.
    Args:
        item_list: any list
        index: the index we want to start looking from
        num_steps: the number of steps to take forward
    Returns:
        a (index, element) tuple such that element is the member of the list
            at index index and the returned index is num_steps larger than the
            given index.
    Example:
        [7, 8, 9], 0, 2 -> (2, 9)
        [7, 8, 9], 2, 1 -> None
    """
    new_index = index + num_steps
    if new_index > len(item_list) - 1:
        return None
    return (new_index, item_list[new_index])


def format_entry(entry_name, opts):
    """
    Look up the entry name from opts, and format its name and value to string
    ready to be written to the alm file.
    Args:
        entry_name: The name of the entry that must also be a key in opts.
        opts: A dictionary prepared by almopts.prepare_default_opts() and
            populated by the user. Contains the value of the entry.
    Returns:
        A string formatted adequately to be written to the alm file.
    Example:
        opts["data"] = [1,2,3]
        format_entry("data", opts) = "data 1 2 3\n"
    """
    target = []
    target.append(entry_name)
    target.append(" ")
    target.append(arr2str(opts[entry_name]))
    target.append("\n")

    return "".join(target)


def format_section(section_name, opts):
    """
    Provide a string representation of arr suitable to be written as a section
    body in the alm file.
    Args:
        section_name: the name of the section that must also be a key in opts.
        opts: A dictionary prepared by almopts.prepare_default_opts() and
            populated by the user. Contains the value of the section.
    Returns:
        A string representation of arr formatted to be written into a section
            in an alm file.
    Example:
        opts["data"] = [[1, 0],[2, 0],[3, 0]]
        format_section("data", opts) =
            "\nBEGIN_DATA\n1 0\n2 0\n3 0\nEND_DATA\n"
    """
    section_str = opts[section_name]
    if datadim(section_str) == 1:
        section_str = [[x] for x in section_str]
    section_name = section_name.upper()
    target = []
    target.append("\nBEGIN_" + section_name + "\n")
    target.append(arr2str(section_str))
    target.append("\nEND_" + section_name + "\n")

    return "".join(target)


def parse_term_code(alm_stdout):
    """
    Given the stdout string from the ALAMO executable, parse the termination
        code.
    Args:
        alm_stdout: A string captured from stdout through running the ALAMO
            executable.
    Returns:
        The termination code codified in the argument string. If no code is in
            the string, that means ALAMO has run successfully: return 0.
    """
    lines = alm_stdout.split("\n")
    for line in lines:
        if "ALAMO terminated with termination code" in line:
            return int(line.split()[-1])
    return 0


def vector_2d(arr):
    """
    Given any array, return a 2D representation of it.
    Example:
        1 -> [[1]]
        [1, 2, 3] -> [[1], [2], [3]]
        [[1], [2], [3]] -> [[1], [2], [3]]
    """
    dim = np.asarray(arr).ndim
    if dim == 0:
        # 0D array (singleton)
        return [[arr]]
    if dim == 1:
        # 1D array
        return [[x] for x in arr]
    # For 2d array, need to deep-convert to python list
    return [[x for x in item] for item in arr]


def get_alamo_version():
    """
    Get the version of alamo.
    Returns: The version number, e.g. 2020.5.27
    """
    exec_result = subprocess.run(
        [str(exec_path)], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    alm_stdout = exec_result.stdout.decode("utf-8")
    lines = alm_stdout.split("\n")
    for line in lines:
        if "ALAMO version" in line:
            return line.split()[2][:-1]
    return 0
