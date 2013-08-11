from django.conf import settings
from django.test import TestCase
#from django.test.client import RequestFactory

from critique.middleware import CritiqueMiddleware


class Request(object):
    def __init__(
            self, method="GET", content_type="text/html", path="/"):
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
        response = response.lower()
        try:
            response.index('<div id="dj-critique">')
        except ValueError:
            return False
        else:
            return True


class ConfigureSettings(CritiqueTestCase):
    def test_custom_settings_type_invalid(self):
        setattr(settings, "CRITIQUE", set())
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings, self.critique.default_settings)
        # @todo check for logging entry

    def test_custom_settings_type_ok(self):
        setattr(settings, "CRITIQUE", {"cancel_text": "EXIT"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["cancel_text"], "EXIT")

    def test_theme_invalid(self):
        setattr(settings, "CRITIQUE", {"theme": "Denver"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["theme"], "light")
        # @todo check for logging entry

    def test_theme_ok(self):
        setattr(settings, "CRITIQUE", {"theme": "dark"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["theme"], "dark")


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
    def test_is_active_invalid(self):
        request = Request()
        request.method = "POST"
        response = self.critique.process_response(request, Response())
        self.assertFalse(self.was_injected(response.content))

#    def test_is_active_ok(self):
#        self.critique.is_active = True
#        response = self.critique.process_response(Request(), Response())
#        self.assertTrue(self.was_injected(response.content))

    def test_response_code_invalid(self):
        self.critique.is_active = True
        response = Response(status_code=302)
        response = self.critique.process_response(Request(), response)
        self.assertFalse(self.was_injected(response.content))

#    def test_response_code_ok(self):
#        self.critique.is_active = True
#        response = self.critique.process_response(Request(), Response())
#        self.assertTrue(self.was_injected(response.content))

#    def test_injection_invalid(self):
#        self.critique.is_active = True
#        self.assertRaises(
#            Exception, self.critique.process_response, Request(), Response())

#    def test_injection_ok(self):
#        self.critique.is_active = True
#        response = self.critique.process_response(Request(), Response())
#        self.assertTrue(self.was_injected(response.content))


class InjectCSS(CritiqueTestCase):
    def test_index_not_found(self):
        self.critique.is_active = True
        self.assertRaises(
            ValueError, self.critique._inject_css, "<html></html>")

    def test_index_ok(self):
        self.critique.is_active = True
        self.critique._inject_css("<html><head></head></html>")

#    def test_template_ok(self):
#        pass


class InjectHTML(CritiqueTestCase):
    def test_index_not_found(self):
        self.critique.is_active = True
        self.assertRaises(
            ValueError, self.critique._inject_html, "<html></html>", Request())

    def test_index_ok(self):
        self.critique.is_active = True
        self.critique._inject_html("<body></body>", Request())


class RenderForm(CritiqueTestCase):
    def test_initial_data(self):
        self.critique.is_active = True
        content = self.critique._render_form(Request())
        content.index('value="Email"')
        content.index('Message</textarea>')

#    def test_template_ok(self):
#        pass
