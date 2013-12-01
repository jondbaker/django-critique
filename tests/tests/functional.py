from time import sleep

from django.conf import settings
from django.test import LiveServerTestCase

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


# determine the WebDriver module; default to FireFox
try:
    web_driver_module = settings.SELENIUM_WEBDRIVER
except AttributeError:
    from selenium.webdriver.firefox import webdriver as web_driver_module


class CustomWebDriver(web_driver_module.WebDriver):
    def find_css(self, css_selector):
        """
        Finds elements by CSS selector. Returns either a list or singleton.
        """
        elems = self.find_elements_by_css_selector(css_selector)
        if len(elems) == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=7):
        """Wraps WebDriverWait."""
        try:
            return WebDriverWait(self, timeout).until(
                lambda driver: driver.find_css(css_selector))
        except:
            self.quit()


class SeleniumTestCase(LiveServerTestCase):
    def open(self, url=None):
        if url is not None:
            self.wd.get("{0}{1}".format(self.live_server_url, url))
        else:
            self.wd.get("{0}{1}".format(self.live_server_url, "/test/"))


class UI(SeleniumTestCase):
    def setUp(self):
        self.cancel = self.wd.find_element_by_id("dj-critique-cancel")
        self.email = self.wd.find_element_by_id("dj-critique-email")
        self.feedback = self.wd.find_element_by_id("dj-critique-feedback")
        self.message = self.wd.find_element_by_id("dj-critique-message")
        self.panel = self.wd.find_element_by_id("dj-critique-create")
        self.prompt = self.wd.find_element_by_id("dj-critique-prompt")
        self.submit = self.wd.find_element_by_id("dj-critique-submit")


class HandheldUI(UI):
    def setUp(self):
        self.wd = CustomWebDriver()
        self.wd.set_window_size(320, 480)
        self.open()
        super(HandheldUI, self).setUp()

    def tearDown(self):
        self.wd.quit()

    def _open_panel(self):
        self.prompt.click()
        self.assertTrue(self.panel.is_displayed())

    def test_form_invisible(self):
        self.assertFalse(self.panel.is_displayed())

    def test_form_visible(self):
        self._open_panel()

    def test_click_cancel(self):
        self._open_panel()
        sleep(.25)
        self.cancel.click()
        sleep(.5)
        self.assertFalse(self.panel.is_displayed())

    def test_input_email_empty(self):
        self._open_panel()
        self.email.send_keys("")
        sleep(.25)
        self.submit.click()
        sleep(.5)
        self.assertEqual(self.feedback.text, "Invalid Submission!")
        self.assertEqual(self.email.get_attribute("class"), "dj-critique-error")

    def test_input_email_invalid(self):
        self._open_panel()
        sleep(.25)
        self.email.send_keys("jdb")
        sleep(.25)
        self.submit.click()
        sleep(.5)
        self.assertEqual(self.feedback.text, "Invalid Submission!")
        self.assertEqual(self.email.get_attribute("class"), "dj-critique-error")

    def test_input_message_empty(self):
        self._open_panel()
        sleep(.25)
        self.email.send_keys("test@test.com")
        self.message.send_keys("")
        sleep(.25)
        self.submit.click()
        sleep(.5)
        self.assertEqual(self.feedback.text, "Invalid Submission!")
        self.assertEqual(
            self.message.get_attribute("class"), "dj-critique-error")

    def test_input_email_invalid_message_empty(self):
        self._open_panel()
        sleep(.25)
        self.email.send_keys("test")
        self.message.send_keys("")
        sleep(.25)
        self.submit.click()
        sleep(.25)
        self.assertEqual(self.feedback.text, "Invalid Submission!")
        self.assertEqual(
            self.message.get_attribute("class"), "dj-critique-error")
        self.assertEqual(self.email.get_attribute("class"), "dj-critique-error")

    def test_input_email_and_message_empty(self):
        self._open_panel()
        sleep(.25)
        self.email.send_keys("")
        self.message.send_keys("")
        sleep(.25)
        self.submit.click()
        sleep(.5)
        self.assertEqual(self.feedback.text, "Invalid Submission!")
        self.assertEqual(
            self.message.get_attribute("class"), "dj-critique-error")
        self.assertEqual(self.email.get_attribute("class"), "dj-critique-error")

    def test_input_ok(self):
        self._open_panel()
        sleep(.25)
        self.email.send_keys("test@test.com")
        self.message.send_keys("Test message")
        sleep(.25)
        self.submit.click()
        sleep(.25)
        self.assertEqual(self.feedback.text, "Success!")

    def test_persists_email(self):
        self._open_panel()
        sleep(.25)
        self.email.send_keys("test@test.com")
        self.message.send_keys("Test message")
        sleep(.25)
        self.submit.click()
        sleep(2)
        self.assertEqual(self.feedback.text, "Success!")
        sleep(3)
        self._open_panel()
        sleep(.5)
        self.assertEqual(self.email.get_attribute("value"), "test@test.com")
