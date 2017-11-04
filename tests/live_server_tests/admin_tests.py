from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

class AdminTests(StaticLiveServerTestCase):


    @classmethod
    def setUpClass(cls):
        super(AdminTests, cls).setUpClass()
        User.objects.create_superuser(username='admin',
                                      password='pw',
                                      email='info@lincolnloop.com')
        cls.selenium = WebDriver(executable_path= '/usr/local/bin/geckodriver')
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(AdminTests, cls).tearDownClass()

    def test_login_wrong_password(self):
        """
        Django Admin login test
        """
        # Open the admin index page
        self.selenium.get(self.live_server_url + reverse('admin:index'))
        # Selenium knows it has to wait for page loads (except for AJAX requests)
        # so we don't need to do anything about that, and can just
        # call find_css. Since we can chain methods, we can
        # call the built-in send_keys method right away to change the
        # value of the field
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys("admin")
        # for the password, we can now just call find_css since we know the page
        # has been rendered
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('pw2')
        # You're not limited to CSS selectors only, check
        # http://seleniumhq.org/docs/03_webdriver.html for
        # a more compreehensive documentation.
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        # Again, after submiting the form, we'll use the find_css helper
        # method and pass as a CSS selector, an id that will only exist
        # on the index page and not the login page
        element = self.selenium.find_element_by_xpath('//*[@id="content"]/p')
        message = 'Please enter the correct username and password for a staff account. ' \
                  'Note that both fields may be case-sensitive.'
        self.assertEqual(element.text, message)


