#!/usr/bin/env python3
"""
actual entry point of the application
"""


from . import constants


def main(args: list) -> int:
    """

    :param args: the command line arguments
    :return: integer return code of the overall application
    """
    return_code = constants.ExitCode.SUCCESS.value

    return return_code
