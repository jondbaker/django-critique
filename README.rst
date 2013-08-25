===============
django-critique
===============
.. image:: https://travis-ci.org/jondbaker/django-critique.png

A responsive, lightweight, unobtrusive, page-by-page critique application for
Django.

Installation
============
#. Until everything is packaged up, the easiest way to install the application
   is with Pip: ``pip install -e git+https://github.com/jondbaker/django-critique.git#egg=django_critique``

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

#. Run ``python manage.py syncdb`` to install the Critique database table.

Requirements
------------

* Python 2.6 or 2.7
* Django 1.5+

Configuration
=============
Critique has a handful of settings that can be set in ``settings.py``::
        
        CRITIQUE = {
            "cancel_text": "Cancel",
            "error_text": "Error!",
            "invalid_text": "Invalid Submission",
            "prompt_text": "Critique this page",
            "submit_text": "Submit",
            "success_text": "Success!",
            "theme": "light"
        }

#. ``cancel_text``
   The string to display on the cancel button; defaults to 'Cancel'.

#. ``error_text``
   The string to display when an AJAX error occurs; defaults to 'Error!'.

#. ``invalid_text``
   The string to display when a submission is invalid; defaults to 'Invalid Submission!'.

#. ``prompt_text``
   The string to display on the always-visible prompt; defaults to 'Critique this page'.

#. ``submit_text``
   The string to display on the submit button; defaults to 'Submit'.

#. ``success_text``
   The string to display when a submission is valid; defaults to 'Success!'.

#. ``theme``
   The CSS theme to use; current options include 'light' and 'dark'; defaults to 'light'. 

Tests
=====
Critique includes a test suite composed of functional, integration and unit
tests. If you commit code, please considering adding proper coverage
(especially if it has a chance for a regression) in the test suite.

::

    $ python setup.py test 

Issues
======
You can report issues at https://github.com/jondbaker/django-critique/issues

Versioning
==========
Semantic Versioning http://semver.org/
