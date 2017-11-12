"""The code for the service which feeds the puzzle
"""

from h2 import config
from h2 import connection
from h2 import events

from twisted.internet import defer, protocol, address
from twisted.python import log


class Response:

    def __init__(self, headers: tuple, body: bytes=b"", trailers: tuple=None):
        self.headers = headers
        self.body = body
        self.trailers = trailers

    def __repr__(self):
        return "<{}: headers:{!r} body:{!r} trailers:{!r}>".format(
            self.__class__.__name__,
            self.headers,
            self.body[:50],
            self.trailers
        )


class BusinesscardProtocol(protocol.Protocol):
    """

    """

    READ_CHUNK_SIZE = 8192

    def __init__(self, peer_address: address.IPv4Address):
        """

        :param peer_address:
        """
        configuration = config.H2Configuration(client_side=False)
        self.conn = connection.H2Connection(config=configuration)
        self.known_proto = None
        self.peer_address = peer_address

        self._flow_control_deferreds = {}

        self.request_handlers = {
            b"BCARD": {
                b"/": self.handle_bcard,
            },
        }

    def connectionMade(self):
        self.conn.initiate_connection()
        self.transport.write(self.conn.data_to_send())

    def dataReceived(self, data):
        if not self.known_proto:
            self.known_proto = True

        ready_events = self.conn.receive_data(data)
        if self.conn.data_to_send:
            self.transport.write(self.conn.data_to_send())

        for event in ready_events:
            if isinstance(event, events.RequestReceived):
                self.request_received(dict(event.headers), event.stream_id)
            elif isinstance(event, events.DataReceived):
                self.data_frame_recieved(event.stream_id)
            elif isinstance(event, events.WindowUpdated):
                self.window_updated(event)

    def data_frame_recieved(self, stream_id):
        self.conn.reset_stream(stream_id)
        self.transport.write(self.conn.data_to_send())

    def window_updated(self, event):
        """
        Handle a WindowUpdated event by firing any waiting data sending
        callbacks.
        """
        stream_id = event.stream_id

        if stream_id and stream_id in self._flow_control_deferreds:
            d = self._flow_control_deferreds.pop(stream_id)
            d.callback(event.delta)
        elif not stream_id:
            for d in self._flow_control_deferreds.values():
                d.callback(event.delta)

            self._flow_control_deferreds = {}

    def wait_for_flow_control(self, stream_id):
        """
        Returns a Deferred that fires when the flow control window is opened.
        """
        d = defer.Deferred()
        self._flow_control_deferreds[stream_id] = d
        return d

    def request_received(self, headers: dict, stream_id: int) -> None:
        """

        :param headers:
        :param stream_id:
        :return:
        """

        method = headers.get(b":method", None)
        path = headers.get(b':path', None)

        method_group = self.request_handlers.get(method, None)
        if method_group is not None:
            matched_path_handler_result = [k for k in method_group.keys()
                                           if path.startswith(k)]
            if 0 < len(matched_path_handler_result):
                matched_path_handler_result.sort(key=lambda x: len(x))
                prefix_handler = method_group[matched_path_handler_result[-1]]
                response = prefix_handler(method, path, headers)

            else:
                response = Response(((":status", "404", ), ))
        else:
            response = Response(((":status", "405", ), ))

        log.msg(response,
                "{}:{}".format(self.peer_address.host, self.peer_address.port),
                method, path)

        close_after_body = response.trailers is None
        self.conn.send_headers(stream_id, response.headers)
        if 0 < len(response.body):
            self.conn.send_data(stream_id, response.body,
                                end_stream=close_after_body)
        if not close_after_body:
            self.conn.send_headers(stream_id, response.trailers,
                                   end_stream=True)

        self.transport.write(self.conn.data_to_send())

    def handle_bcard(self, method: bytes, path: bytes, headers: dict
                     ) -> Response:
        """

        :param method:
        :param path:
        :param headers:
        :return:
        """

        return Response(
            (
                (":status", "200", ),
                ("content-length", str(0), ),
                ("name", "Mike Winstead", ),
                ("email", "m@winstead.us", ),
                ("github", "/mrwinstead", ),
                ("blog", "winstead.us/blog"),
                ("Trailer", "X-More-Info",),
            ),
            b"",
            (
                ("X-More-Info", "more info"),
            )
        )


class H2Factory(protocol.Factory):

    def __init__(self):
        pass

    def buildProtocol(self, peer_address: address.IPv4Address):
        return BusinesscardProtocol(peer_address)
