

import http as stdlib_http

from django import http

_BUSINESS_CARD_HEADERS = {
    "name": "Mike Winstead",
    "email": "mike<at>wintead<dot>us",
    "github": "/mrwinstead",
    "blog": "mrwinstead.blogspot.com",
}


def index(request: http.HttpRequest) -> http.HttpResponse:
    """
    This is the landing page for the puzzle. If the user doesn't give the
    correct request verb (BCARD), we just 204 them. If they have "BCARD" as the
    verb, then we move to give then the appropriate response

    :param request: the inbound request
    :return: response according to conditions described
    """
    response = http.HttpResponse(status=stdlib_http.HTTPStatus.NO_CONTENT)
    if request.method == "BCARD":
        for key in _BUSINESS_CARD_HEADERS.keys():
            # according to [1], this is how you set django headers
            # [1]: https://docs.djangoproject.com/en/1.11/ref/request-response/#setting-header-fields
            response[key] = _BUSINESS_CARD_HEADERS[key]

    return response

