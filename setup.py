#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="django-critique",
    version="0.1.1",
    description="A simple and responsive critique application for Django.",
    long_description=open("README.rst").read(),
    author="Jonathan D. Baker",
    author_email="jonathan@piqueinteractive.com",
    url="https://github.com/jondbaker/django-critique",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Indepdent",
        "Programming Language :: Python",
        "Topic :: Software Development"],
    zip_safe=False,
    install_requires=[
        "django>=1.3.1"],
    tests_require=["Django>=1.4.1", "selenium"],
    test_suite="runtests.runtests",)
