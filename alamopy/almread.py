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
almread.py
Parse a .lst file generated by ALAMO.
"""
from sympy.parsing import parse_expr
from sympy import symbols, lambdify
from alamopy import almutils


def read_lst_file(opts):
    """
    Read the lst file, parse results, and store them into opts["return"].
    Args:
        opts: A dictionary that contains all the options both necessary and 
              optional. 
    """
    # Quick error checking to make sure file exists
    try:
        with open(opts["lst_file_name"], "r") as lst_file:
            lines = [line.strip() for line in lst_file]
    except FileNotFoundError:
        return

    # Reading "in" part
    # Reading listed options
    i, curr = almutils.nets(lines, 0, lambda s: "=" in s)
    this_dict = {}
    while not almutils.only_contains(curr, "="):
        curr_list = curr.split("=")
        entry_name = curr_list[0].strip()
        entry_val = curr_list[-1].strip()
        this_dict[entry_name] = almutils.cast(entry_val)
        i, curr = almutils.increment(lines, i, 1)

    # Reading organized input data, part 1 (XLABELS)
    i, curr = almutils.nets(lines, i, lambda s: "XLABELS" in s)
    entry_list = curr.split()
    for entry_name in entry_list:
        this_dict[entry_name] = []
    i, curr = almutils.increment(lines, i, 1)
    while "ZLABELS" not in curr:
        for (entry_name, entry_val) in zip(entry_list, curr.split()):
            this_dict[entry_name].append(almutils.cast(entry_val))
        i, curr = almutils.increment(lines, i, 1)

    # Reading organized input data, part 2 (ZLABELS)
    i, curr = almutils.nets(lines, i, lambda s: "ZLABELS" in s)
    entry_list = curr.split()
    for entry_name in entry_list:
        this_dict[entry_name] = []
    i, curr = almutils.increment(lines, i, 1)
    while curr != "":
        for (entry_name, entry_val) in zip(entry_list, curr.split()):
            this_dict[entry_name].append(almutils.cast(entry_val))
        i, curr = almutils.increment(lines, i, 1)

    # Reading organized input data, part 3 (XDATA and ZDATA, and all other)
    i, curr = almutils.nets(lines, i, lambda s: "XDATA and ZDATA" in s)
    while not almutils.only_contains(curr, "="):
        i, curr = almutils.nets(lines, i, lambda s: s != "")
        entry_name = curr.strip()
        i, curr = almutils.increment(lines, i, 1)
        entry_list = []
        while not (almutils.only_contains(curr, "=") or curr == ""):
            curr = curr.strip()
            entry_list.append([almutils.cast(x) for x in curr.split()])
            i, curr = almutils.increment(lines, i, 1)
        if len(entry_list) == 1:
            entry_list = entry_list[0]
        this_dict[entry_name] = entry_list

    # Reading bases considered
    i, curr = almutils.nets(lines, i, lambda s: "BASES considered" in s)
    i, curr = almutils.increment(lines, i, 1)
    entry_list = []
    while not almutils.only_contains(curr, "="):
        entry_list.append(almutils.cast(curr.strip()))
        i, curr = almutils.increment(lines, i, 1)
    this_dict["bases"] = entry_list

    # Storing "in" part results into return dict
    opts["return"]["in"] = this_dict

    # Reading "out" part
    # Reading output model
    i, curr = almutils.nets(lines, i, lambda s: "Quality metrics for output" in s)
    # Repeatedly reads for all z variables, if more than one
    while "Quality metrics for output" in curr:
        z_name = curr.split()[-1]
        this_dict = {}
        i, curr = almutils.nets(lines, i, lambda s: ":" in s)

        # Reading all quality metrics
        while ":" in curr:
            entry_name, entry_val = curr.split(":")
            entry_val = entry_val.strip()
            this_dict[entry_name] = almutils.cast(entry_val)
            i, curr = almutils.increment(lines, i, 1)
        i, curr = almutils.nets(
            lines, i, lambda s: "BETAS and BASES chosen for this output" in s
        )

        # Reading the final model
        curr_list = []
        i, curr = almutils.increment(lines, i, 1)
        while curr != "":
            curr_list.append(curr)
            i, curr = almutils.increment(lines, i, 1)
        this_dict["model_str"] = almutils.represent_model_str(curr_list)
        this_dict["model_fun"] = lambdify(
            symbols(opts["return"]["in"]["XLABELS"]),
            parse_expr(this_dict["model_str"].replace("^", "**")),
            "numpy",
        )

        # Storing this z variable into return dict
        opts["return"]["out"][z_name] = this_dict
        i, curr = almutils.nets(lines, i, lambda s: s != "")

    # Reading "other" part
    # Reading time total
    i, curr = almutils.nets(lines, i, lambda s: "Total execution time" in s)
    this_dict = {}
    curr_list = curr.split()
    this_dict["total"] = almutils.cast(curr_list[curr_list.index("s") - 1])
    i, curr = almutils.increment(lines, i, 2)

    # Reading all breakdown entries
    while ":" in curr:
        curr_list = curr.split()
        entry_name = curr_list[curr_list.index("time:") - 1]
        entry_val = almutils.cast(curr_list[curr_list.index("s") - 1])
        this_dict[entry_name] = entry_val
        i, curr = almutils.increment(lines, i, 1)

    # Storing "time" part results into return dict
    opts["return"]["other"]["time"] = this_dict
