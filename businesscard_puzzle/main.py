#!/usr/bin/env python3
"""
actual entry point of the application
"""


import sys


from twisted.internet import endpoints, reactor
from twisted.python import log
from twisted.web import server


from . import constants
from . import service


def main(args: list) -> int:
    """

    :param args: the command line arguments
    :return: integer return code of the overall application
    """
    return_code = constants.ExitCode.SUCCESS.value

    site = server.Site(service.PuzzleResponder())
    endpoint_spec = "ssl:port=8080:privateKey=privkey.pem:certKey=cert.pem"
    endpoint = endpoints.serverFromString(reactor, endpoint_spec)
    endpoint.listen(site)

    log.startLogging(sys.stdout)

    reactor.run()

    return return_code
