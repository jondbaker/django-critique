#from django.conf import settings
from django.test import TestCase
#from django.test.client import RequestFactory

from critique.middleware import CritiqueMiddleware


class Request(object):
    def __init__(self):
        self.method = "GET"
        self.META = {"CONTENT_TYPE": "text/plain"}
        self.path = "/"


class Response(object):
    pass


class CritiqueTestCase(TestCase):
    def setUp(self):
        self.critique = CritiqueMiddleware()


class ProcessRequest(CritiqueTestCase):
    def test_mime_invalid(self):
        request = Request()
        request.META["CONTENT_TYPE"] = "image/jpeg"
        self.critique.process_request(request)
        self.assertFalse(self.critique.is_active)

    def test_mime_ok(self):
        request = Request()
        self.critique.process_request(request)
        self.assertTrue(self.critique.is_active)

    def test_http_method_invalid(self):
        request = Request()
        request.method = "POST"
        self.critique.process_request(request)
        self.assertFalse(self.critique.is_active)

    def test_http_method_ok(self):
        request = Request()
        self.critique.process_request(request)
        self.assertTrue(self.critique.is_active)

    def test_url_invalid(self):
        request = Request()
        request.path = "/admin"
        self.critique.process_request(request)
        self.assertFalse(self.critique.is_active)

    def test_url_ok(self):
        request = Request()
        self.critique.process_request(request)
        self.assertTrue(self.critique.is_active)
