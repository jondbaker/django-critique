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
    def __init__(
            self, status_code=200,
            content="<html><head></head><body></body></html>"):
        """Happy-path settings"""
        self.status_code = status_code
        self.content = content


class CritiqueTestCase(TestCase):
    def setUp(self):
        self.critique = CritiqueMiddleware()

    def assertCritiqueInjected(self, response):
        try:
            response.lower().index('<div id="dj-critique">')
        except ValueError:
            return False
        else:
            return True

    def tearDown(self):
        """Resets settings.CRITIQUE to default values."""
        # not sure why the following line doesn't work...
#        setattr(settings, "CRITIQUE", self.critique.default_settings)
        setattr(settings, "CRITIQUE", {
            "cancel_text": "Cancel",
            "error_text": "Error!",
            "invalid_text": "Invalid Submission!",
            "prompt_text": "Critique this page",
            "submit_text": "Submit",
            "success_text": "Success!",
            "theme": "light"})


class ConfigureSettings(CritiqueTestCase):
    def test_custom_settings_type_invalid(self):
        setattr(settings, "CRITIQUE", set())
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings, self.critique.default_settings)
        # @todo check for logging entry

    def test_cancel_text_setting(self):
        setattr(settings, "CRITIQUE", {"cancel_text": "EXIT"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["cancel_text"], "EXIT")

    def test_error_text_setting(self):
        setattr(settings, "CRITIQUE", {"error_text": "ERROR"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["error_text"], "ERROR")

    def test_invalid_text_setting(self):
        setattr(settings, "CRITIQUE", {"invalid_text": "INVALID"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["invalid_text"], "INVALID")

    def test_prompt_text_setting(self):
        setattr(settings, "CRITIQUE", {"prompt_text": "ACT"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["prompt_text"], "ACT")

    def test_submit_text_setting(self):
        setattr(settings, "CRITIQUE", {"submit_text": "GO"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["submit_text"], "GO")

    def test_success_text_settings(self):
        setattr(settings, "CRITIQUE", {"success_text": "SUCCESS"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["success_text"], "SUCCESS")

    def test_theme_setting_invalid(self):
        setattr(settings, "CRITIQUE", {"theme": "Denver"})
        app_settings = self.critique._configure_settings()
        self.assertEqual(app_settings["theme"], "light")
        # @todo check for logging entry

    def test_theme_setting_ok(self):
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
        self.assertFalse(self.assertCritiqueInjected(response.content))

    def test_is_active_ok(self):
        self.critique.is_active = True
        response = self.critique.process_response(Request(), Response())
        self.assertTrue(self.assertCritiqueInjected(response.content))

    def test_response_code_invalid(self):
        self.critique.is_active = True
        response = Response(status_code=302)
        response = self.critique.process_response(Request(), response)
        self.assertFalse(self.assertCritiqueInjected(response.content))

    def test_response_code_ok(self):
        self.critique.is_active = True
        response = self.critique.process_response(Request(), Response())
        self.assertTrue(self.assertCritiqueInjected(response.content))

    def test_response_markup_invalid(self):
        self.critique.is_active = True
        content = "<html>"
        response = Response()
        response.content = content
        response = self.critique.process_response(Request(), response)
        self.assertEqual(content, response.content)

    def test_response_markup_ok(self):
        self.critique.is_active = True
        response = Response()
        response = self.critique.process_response(Request(), response)
        self.assertTrue(self.assertCritiqueInjected(response.content))


class InjectCSS(CritiqueTestCase):
    def test_index_not_found(self):
        self.critique.is_active = True
        self.assertRaises(
            ValueError, self.critique._inject_css, "<html></html>")

    def test_index_ok(self):
        self.critique.is_active = True
        self.critique._inject_css("<html><head></head></html>")


class InjectHTML(CritiqueTestCase):
    def test_index_not_found(self):
        self.critique.is_active = True
        self.assertRaises(
            AttributeError, self.critique._inject_html, "<html></html>", Request())

    def test_index_ok_body_attr(self):
        self.critique.is_active = True
        self.critique._inject_html('<body class="test"></body>', Request())

    def test_index_ok_body_clean(self):
        self.critique.is_active = True
        self.critique._inject_html("<body></body>", Request())


class InjectJS(CritiqueTestCase):
    def test_index_not_found(self):
        self.critique.is_active = True
        self.assertRaises(
            ValueError, self.critique._inject_js, "<html></html>")

    def test_index_ok(self):
        self.critique.is_active = True
        self.critique._inject_js("<body></body>")


class RenderForm(CritiqueTestCase):
    def test_initial_data(self):
        self.critique.is_active = True
        content = self.critique._render_form(Request())
        content.index('value="Email"')
        content.index('Message</textarea>')
