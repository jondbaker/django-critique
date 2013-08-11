try:
    from django.conf.urls import include, patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.default import include, patterns, url

from .views import TestView

urlpatterns = patterns(
    "",
    url(r"^test/$", TestView.as_view(), name="test_view"),
    url(r"^", include("critique.urls")))
