#!/usr/bin/env python3
"""
actual entry point of the application
"""

import pathlib
import sys

from OpenSSL import crypto

from twisted.internet import reactor, ssl
from twisted.python import log


from businesscard_puzzle import constants
from businesscard_puzzle import service


def main(args: list) -> int:
    """

    :param args: the command line arguments
    :return: integer return code of the overall application
    """
    return_code = constants.ExitCode.SUCCESS.value

    factory = service.H2Factory()

    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                         pathlib.Path(args[0]).read_text())
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM,
                                          pathlib.Path(args[1]).read_text())
    tls_options = ssl.CertificateOptions(
        privateKey=private_key,
        certificate=certificate,
        acceptableProtocols=[b'h2', ]
    )
    reactor.listenSSL(9443, factory, tls_options)
    log.startLogging(sys.stderr)

    reactor.run()

    return return_code
