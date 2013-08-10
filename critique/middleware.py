import logging
import re


class CritiqueMiddleware(object):
    """
    Manages rendering the Critique markup based upon characteristics of the
    incoming request and the outgoing response.
    """
    is_active = None
    mime_types = ["text/plain", "application/xhtml+xml"]

    def _inject(self, request, response):
        return '<div id="dj-critique"></div>'

    def process_request(self, request):
        """Django middleware hook.

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

    def process_response(self, request, response):
        """Django middleware hook.

        :seealso: https://docs.djangoproject/en/1.5/topics/http/middleware/#process-response

        :param request: HTTP request
        :request type: object
        :param request: HTTP response
        :request type: object

        :returns: HTTP response
        :rtype: object
        """
        if self.is_active and response.status_code == 200:
            try:
                response.content = self._inject(request, response)
            except Exception as e:
                logging.debug("Exception: " + repr(e))
        return response
