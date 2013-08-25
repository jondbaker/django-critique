===============
django-critique
===============
.. image:: https://travis-ci.org/jondbaker/django-critique.png

A responsive, page-by-page critique application for Django.

Installation
============
#. Until everything is packaged up, the easiest way to install the application
   is to use Pip to install the Git repo: ``pip install -e git+https://github.com/jondbaker/django-critique.git#egg=django_critique``

#. Configure ``INSTALLED_APPS`` and ``MIDDLEWARE_CLASSES``::

        INSTALLED_APPS = (
            ...
            "critique",
        )

        MIDDLEWARE_CLASSES = (
            ...
            "critique.middleware.CritiqueMiddleware",
        )

#. Include URLs::

        urlpatterns = patterns(""
            ...
            url(r"^", include("critique.urls")),
        )

#. Run ``python manage.py syncdb`` to install the Critique model table.

Requirements
------------

* Django 1.3+

Configuration
=============
Critique has four optional settings that can be set in ``settings.py``::
        
        CRITIQUE = {
            "cancel_text": "Cancel",
            "prompt_text": "Critique this page",
            "submit_text": "Submit",
            "theme": "light"
        }

#. ``cancel_text``
   The string to use on the cancel button. Defaults to 'Cancel'.

#. ``prompt_text``
   The string to use for the always-visible prompt. Defaults to 'Critique this page'.

#. ``submit_text``
   The string to use on the submit button. Defaults to 'Submit'.

#. ``theme``
   The CSS theme to use. Current options include 'light' and 'dark'. Defaults to 'light'. 

Tests
=====
Critique includes a limited (but growing) test suite. If you commit code,
please considering adding proper coverage (especially if it has a chance for a
regression) in the test suite.

::

    $ python setup.py test 

Issues
======
You can report issues at https://github.com/jondbaker/django-critique/issues

Versioning
==========
Semantic Versioning http://semver.org/
