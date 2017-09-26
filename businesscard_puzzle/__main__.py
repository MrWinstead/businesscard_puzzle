#!/usr/bin/env python3
"""module to call main and exit with its return code
"""


import sys

from . import main

sys.exit(
    main.main(
        sys.argv[1:]
    )
)
