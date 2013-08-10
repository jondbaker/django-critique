#from django.conf import settings
from django.test import TestCase
#from django.test.client import RequestFactory

from critique.middleware import CritiqueMiddleware


class Request(object):
    def __init__(
            self, method="GET", content_type="text/plain", path="/"):
        """Happy-path settings"""
        self.method = method
        self.META = {"CONTENT_TYPE": content_type}
        self.path = path


class Response(object):
    def __init__(self, status_code=200):
        """Happy-path settings"""
        self.status_code = status_code
        self.content = ""


class CritiqueTestCase(TestCase):
    def setUp(self):
        self.critique = CritiqueMiddleware()

    def was_injected(self, response):
        try:
            response.lower().index('<div id="dj-critique">')
        except ValueError:
            return False
        else:
            return True


class ProcessRequest(CritiqueTestCase):
    def test_http_method_invalid(self):
        request = Request(method="POST")
        self.critique.process_request(request)
        self.assertFalse(self.critique.is_active)

    def test_http_method_ok(self):
        request = Request()
        self.critique.process_request(request)
        self.assertTrue(self.critique.is_active)

    def test_mime_invalid(self):
        request = Request(content_type="image/jpeg")
        self.critique.process_request(request)
        self.assertFalse(self.critique.is_active)

    def test_mime_ok(self):
        request = Request()
        self.critique.process_request(request)
        self.assertTrue(self.critique.is_active)

    def test_url_invalid(self):
        request = Request(path="/admin")
        self.critique.process_request(request)
        self.assertFalse(self.critique.is_active)

    def test_url_ok(self):
        request = Request()
        self.critique.process_request(request)
        self.assertTrue(self.critique.is_active)


class ProcessResponse(CritiqueTestCase):
#    def test_inject_invalid(self):
#        # @todo need to pass poorly-formed HTML to raise Exception
#        self.critique.is_active = True
#        self.assertRaises(
#            Exception, self.critique.process_response, Request(), Response())

#    def test_inject_ok(self):
#        pass

    def test_is_active_invalid(self):
        request = Request()
        request.method = "POST"
        response = self.critique.process_response(request, Response())
        self.assertFalse(self.was_injected(response.content))

    def test_is_active_ok(self):
        self.critique.is_active = True
        response = self.critique.process_response(Request(), Response())
        self.assertTrue(self.was_injected(response.content))

    def test_response_code_invalid(self):
        self.critique.is_active = True
        response = Response(status_code=302)
        response = self.critique.process_response(Request(), response)
        self.assertFalse(self.was_injected(response.content))

    def test_response_code_ok(self):
        self.critique.is_active = True
        response = self.critique.process_response(Request(), Response())
        self.assertTrue(self.was_injected(response.content))
