from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from critique.models import Critique


class CritiqueCreate(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_domain = "http://testserver"

    def test_get(self):
        """404"""
        response = self.client.get(reverse("critique_create"))
        self.assertEqual(response.status_code, 404)

    def test_non_ajax(self):
        """404"""
        response = self.client.post(reverse("critique_create"), data={})
        self.assertEqual(response.status_code, 404)

    def test_post_empty_email(self):
        """200"""
        response = self.client.post(
            reverse("critique_create"), data={"email": "", "message": "test"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "ERROR")

    def test_post_invalid_email(self):
        """200"""
        response = self.client.post(
            reverse("critique_create"), data={"email": "0", "message": "test"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "ERROR")

    def test_post_empty_message(self):
        """200"""
        response = self.client.post(
            reverse("critique_create"),
            data={"email": "test@test.com", "message": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "ERROR")

    def test_post_ok(self):
        """200"""
        len_pre = Critique.objects.all().count()
        response = self.client.post(
            reverse("critique_create"),
            data={"email": "test@test.com", "message": "test"},
            HTTP_REFERER="/test/", HTTP_USER_AGENT="test",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "OK")
        self.assertEqual(len_pre + 1, Critique.objects.all().count())
