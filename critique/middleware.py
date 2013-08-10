import re


class CritiqueMiddleware(object):
    """
    Manages rendering the Critique markup based upon characteristics of the
    incoming request and the outgoing response.
    """
    is_active = None
    mime_types = ["text/plain", "application/xhtml+xml"]

    def process_request(self, request):
        """Middleware hook.

        :seealso: https://docs.djangoproject/en/1.5/topics/http/middleware/#process-request

        :param request: HTTP request
        :request type: object

        :returns: None
        :rtype: None
        """
        self.is_active = False
        if (request.method == "GET" and
                request.META["CONTENT_TYPE"] in self.mime_types and
                not re.match("^/admin", request.path)):
            self.is_active = True
        return None
