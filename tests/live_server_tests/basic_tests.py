from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver


class CalculatorTests(StaticLiveServerTestCase):


    @classmethod
    def setUpClass(cls):
        super(CalculatorTests, cls).setUpClass()
        User.objects.create_superuser(username='admin',
                                      password='pw',
                                      email='info@lincolnloop.com')


    @classmethod
    def tearDownClass(cls):

        super(CalculatorTests, cls).tearDownClass()

    def setUp(self):
        self.selenium = WebDriver(executable_path='/usr/local/bin/geckodriver')
        self.selenium.implicitly_wait(10)
        print('<<<< SETUP')

    def tearDown(self):
        #self.selenium.quit()
        print('<<<< TD')

    def test_calculator(self):
        """
        Django Admin login test
        """
        # Open the admin index page
        self.selenium.get(self.live_server_url + reverse('calendar:calculator'))
        # Selenium knows it has to wait for page loads (except for AJAX requests)
        # so we don't need to do anything about that, and can just
        # call find_css. Since we can chain methods, we can
        # call the built-in send_keys method right away to change the
        # value of the field
        self.selenium.find_element_by_xpath('//*[@id="id_start_date"]').send_keys(4 * Keys.BACKSPACE)
        self.selenium.find_element_by_xpath('//*[@id="id_start_date"]').send_keys("2017-10-01")
        # for the password, we can now just call find_css since we know the page
        # has been rendered
        self.selenium.find_element_by_xpath('//*[@id="id_end_date"]').send_keys(4 * Keys.BACKSPACE)
        self.selenium.find_element_by_xpath('//*[@id="id_end_date"]').send_keys('2017-10-31')
        # You're not limited to CSS selectors only, check
        # http://seleniumhq.org/docs/03_webdriver.html for
        # a more compreehensive documentation.
        self.selenium.find_element_by_xpath('/html/body/div[2]/form/input[2]').click()
        # /html/body/div[2]/form/input[2]
        element = self.selenium.find_element_by_xpath('/html/body/div[2]/h3')  # /html/body/div[2]/form/input[2]
        message = '22 working days'
        self.assertEqual(element.text, message)

    # def test_calculator_error(self):
    #     """
    #    html body div.container div.alert.alert-error
    #     """
    #     # Open the admin index page
    #     self.selenium.get(self.live_server_url)
    #     self.selenium.get(self.live_server_url + reverse('calendar:calculator'))
    #     # Selenium knows it has to wait for page loads (except for AJAX requests)
    #     # so we don't need to do anything about that, and can just
    #     # call find_css. Since we can chain methods, we can
    #     # call the built-in send_keys method right away to change the
    #     # value of the field
    #     self.selenium.find_element_by_xpath('//*[@id="id_start_date"]').send_keys(4 * Keys.BACKSPACE)
    #     self.selenium.find_element_by_xpath('//*[@id="id_start_date"]').send_keys("2017-10-01")
    #     # for the password, we can now just call find_css since we know the page
    #     # has been rendered
    #     self.selenium.find_element_by_xpath('//*[@id="id_end_date"]').send_keys(4 * Keys.BACKSPACE)
    #     self.selenium.find_element_by_xpath('//*[@id="id_end_date"]').send_keys('2018-10-31')
    #     # You're not limited to CSS selectors only, check
    #     # http://seleniumhq.org/docs/03_webdriver.html for
    #     # a more compreehensive documentation.
    #     self.selenium.find_element_by_xpath('/html/body/div[2]/form/input[2]').click()
    #     self.selenium.implicitly_wait(5)
    #     element = self.selenium.find_elements(By.CLASS_NAME, "alert")[0]
    #     message = 'End date exceed the last registered holiday'
    #     self.assertEqual(element.text, message)
