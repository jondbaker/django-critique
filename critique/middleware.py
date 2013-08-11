import logging
import re

from django.conf import settings
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _


class CritiqueMiddleware(object):
    """
    Manages rendering the Critique markup based upon characteristics of the
    incoming request and the outgoing response.
    """
    default_settings = {
        "cancel_text": _("Cancel"),
        "prompt_text": _("Critique this page"),
        "submit_text": _("Submit"),
        "theme": "light"}
    is_active = None
    mime_types = ["text/html"]
    static_url = getattr(settings, "STATIC_URL", "/")
    themes = ["dark", "light"]

    def __init__(self):
        self.settings = self._configure_settings()

    def _configure_settings(self):
        """Configures application settings

        :returns: application settings
        :rtype: dict
        """
        app_settings = self.default_settings
        user_settings = getattr(settings, "CRITIQUE", {})
        user_settings_type = type(user_settings)

        if user_settings_type is not dict:
            logging.debug(
                "settings.CRITIQUE must be type dict and not {0}".format(
                    user_settings_type))

        elif user_settings_type is dict and user_settings:
            app_settings.update(user_settings)

            # validate theme
            if app_settings["theme"] not in self.themes:
                logging.debug(
                    "Unknown theme {0}; defaulting to 'light'.".format(
                        app_settings["theme"]))
                app_settings["theme"] = "light"

        return app_settings

    def _inject_css(self, content):
        """Injects CSS markup

        :returns: HTTP response content
        :rtype: string
        """
        target = "</head>"
        index = content.lower().rindex(target)
        template = loader.get_template("critique/_css.html")
        markup = template.render(Context({
            "static_url": self.static_url,
            "theme": self.settings["theme"]}))
        return content[:index] + markup + content[index:]

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
                content = self._inject_css(response.content)
#                content = self._inject_html(content, request)
#                content = self._inject_js(content)
            except Exception as e:
                logging.debug("Exception: " + repr(e))
            else:
                response.content = content
        return response
