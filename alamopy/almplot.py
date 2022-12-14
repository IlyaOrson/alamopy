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
Plot doalamo output including confidence intervals if they are calculated.
    Args:
        res: A dictionary that contains the results from the ALAMO running
        show: defaulted to be true, unless indicated as false so plots are NOT SHOWN
"""


def almplot(res, show=True):
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        #  from alamopy.writethis import writethis
    except Exception:
        print("Cannot plot, possibly missing matplotlib package")

    model = res["model"].replace(" - ", " + -")
    model = model.split("=")[1]
    model = model.split(" + ")
    if model[0] == " ":  # if there are more than one terms, the first split is ' '
        model = model[1:]
    ndp = 100
    t = np.linspace(0.08, 1.7, ndp)
    out = np.zeros([3, ndp])
    clo = np.zeros(ndp)
    chi = np.zeros(ndp)
    coeff = np.zeros(ndp)

    for i in range(len(model)):
        coeff[i] = float(model[i].split(" * ")[0])
        if "conf_inv" in res.keys():
            clo[i] = coeff[i] - float(res["conf_inv"][i].split("+/-")[1])
            chi[i] = coeff[i] + float(res["conf_inv"][i].split("+/-")[1])

    for i in range(ndp):
        out[0, i] = (
            float(coeff[0]) * t[i] ** 1.2
            - float(coeff[1]) * t[i] ** 2
            - float(coeff[2])
        )
        if "conf_inv" in res.keys():  # If confidence intervals exist
            out[1, i] = clo[0] * t[i] ** 1.2 - chi[1] * t[i] ** 2 - chi[2]
            out[2, i] = chi[0] * t[i] ** 1.2 - clo[1] * t[i] ** 2 - clo[2]

    plt.plot(t, out[0], "b-")
    if "conf_inv" in res.keys():
        plt.plot(t, out[1], "r--", t, out[2], "r--")
    if show:
        plt.show()
