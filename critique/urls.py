try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.default import patterns, url

from .views import create

urlpatterns = patterns(
    "",
    url(r"^critique/create/$", create, name="critique_create"))
