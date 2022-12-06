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
almexec.py
Run the ALAMO executable.
"""

import subprocess
import alamopy.almutils as almutils
from pathlib import Path

base_path = Path.home()
# base_path = Path("/home/io")  # wsl
# base_path = Path("/content/")  # collab

exec_path = base_path / "alamo-linux64" / "alamo"

print(f"Expected ALAMO executable location: {exec_path}")

def exec_alamo(opts):
    """
    Call ALAMO on the written alm file, and capture stdout and stderr.
    """
    exec_result = subprocess.run(
        # [exec_path, opts["alm_file_name"]],
        [str(exec_path), opts["alm_file_name"]],
        check=True,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        shell=True,
        capture_output=True,
    )
    print(exec_result.stderr)
    alm_out = exec_result.stdout.decode("utf-8")
    opts["return"]["other"]["return_code"] = almutils.parse_term_code(alm_out)

    if opts["print_alm_output"]:
        print(alm_out)
