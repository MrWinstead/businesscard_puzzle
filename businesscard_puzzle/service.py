"""The code for the service which feeds the puzzle
"""

from twisted.python import log
from twisted.web import resource


class PuzzleResponder(resource.Resource):
    """

    """

    isLeaf = True

    def render_GET(self, request):
        """

        :param request:
        :return:
        """
        log.msg("%r %r" % (type(request), request))
        return b"hello world"
