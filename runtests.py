#!/usr/bin/env python
import os
import sys

from django.conf import settings, global_settings

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3"}},
        DEBUG=True,
        INSTALLED_APPS=[
            "critique",
            "tests",
        ],
        MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES + (
            "critique.middleware.CritiqueMiddleware",),
        ROOT_URLCONF="tests.urls",
        STATIC_URL="/static/",
        TEMPLATE_DIRS=(os.path.join(PROJECT_ROOT, "tests", "templates"))
    )


def runtests(*test_args):
    if not test_args:
        test_args = ["tests"]

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(
        verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests()
