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


def almconfidence(data, *vargs):
    # This function calulates a covariance matrix
    # and confidence intervals of the estimated alamo regression coeficients
    """
    This function calulates a covariance matrix
    and confidence intervals of the estimated alamo regression coefficients
    Args:
        data: A dictionary that contains the values necessary to create
              the confidence interval. It is produced when ALAMO is run
              and returns back the metrics.
    """
    import numpy as np

    # import sympy
    from scipy.stats import t  # 2.7
    from sympy.parsing.sympy_parser import parse_expr
    from sympy import symbols, lambdify

    if "xdata" not in data.keys():
        xdata = vargs[0]
        # zdata = vargs[1]
    else:
        xdata = data["xdata"]
        # zdata = data['zdata']

    ndata = np.shape(xdata)[0]
    # ninputs = np.shape(xdata)[1]
    # noutputs = np.shape(zdata)[1]
    if isinstance(data["model"], type({})):
        for okey in data["model"].keys():
            model = data["model"][okey]
            model.split("=")[1]
            # out = model.split('=')[0]
            model = model.split("=")[1]
            # split the model on +/- to isolate each linear term
            # This section is not currently in compliance with custom basis functions
            model = model.replace(" - ", " + ").split(" + ")
            nlinterms = len(model)
            sensmat = np.zeros([ndata, nlinterms])
            covar = np.zeros([nlinterms, nlinterms])
            coeffs = np.zeros([nlinterms])
            for j in range(nlinterms):
                thisterm = model[j].split(" * ")
                coeffs[j] = float(eval(thisterm[0]))
                thisterm = thisterm[-1]
                thislam = lambdify(
                    [symbols(data["xlabels"])],
                    parse_expr(thisterm.replace("^", "**")),
                    "numpy",
                )
                for i in range(ndata):
                    sensmat[i, j] = thislam(xdata[i])

            sigma = float(data["ssr"]) / (float(ndata) - float(nlinterms))
            ci = np.zeros([nlinterms])
            covar = sigma * np.linalg.inv(np.matmul(np.transpose(sensmat), sensmat))
            for i in range(0, nlinterms):
                ci[i] = t.ppf(1 - 0.025, int(ndata) - nlinterms) * np.sqrt(covar[i][i])

            data["covariance"][okey] = covar
            data["conf_inv"][okey] = list()
            for j in range(nlinterms):
                data["conf_inv"][okey].append(
                    "B" + str(j + 1) + " : " + str(coeffs[j]) + "+/-" + str(ci[j])
                )
    else:
        model = data["model"]
        model.split("=")[1]
        # out = model.split('=')[0]
        model = model.split("=")[1]
        # split the model on +/- to isolate each linear term
        # This section is not currently in compliance with custom basis functions
        model = model.replace(" - ", " + ").split(" + ")
        while "" in model:
            model.remove("")
        while " " in model:
            model.remove(" ")
        nlinterms = len(model)
        sensmat = np.zeros([ndata, nlinterms])
        covar = np.zeros([nlinterms, nlinterms])
        coeffs = np.zeros([nlinterms])
        for j in range(nlinterms):
            if " * " in model[j]:
                thisterm = model[j].split(" * ")
                coeffs[j] = float(eval(thisterm[0]))
                thisterm = thisterm[-1]
            else:
                thisterm = model[j]
                coeffs[j] = float(eval(thisterm))
            thislam = lambdify(
                [symbols(data["xlabels"])],
                parse_expr(thisterm.replace("^", "**")),
                "numpy",
            )
            for i in range(ndata):
                sensmat[i, j] = thislam(xdata[i])

        sigma = float(data["ssr"]) / (float(ndata) - float(nlinterms))

        covar = sigma * np.linalg.inv(np.matmul(np.transpose(sensmat), sensmat))
        ci = np.zeros([nlinterms])
        for i in range(0, nlinterms):
            ci[i] = t.ppf(1 - 0.025, int(ndata) - nlinterms) * np.sqrt(
                covar[i][i]
            )  # 2.7

        data["covariance"] = covar
        data["conf_inv"] = list()
        for j in range(nlinterms):
            data["conf_inv"].append(
                "B" + str(j + 1) + " : " + str(coeffs[j]) + "+/-" + str(ci[j])
            )
        return data
