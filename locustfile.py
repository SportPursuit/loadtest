import requests
import random
import time

from realbrowserlocusts import PhantomJSLocust, FirefoxLocust

from locust import TaskSet, task
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LocustUserBehavior(TaskSet):

    def _signup(self):
        self.username = self._generate_test_email_address() 
        self.client.implicitly_wait(10)
        self.client.get('https://www.sportpursuit-stage.com/customer/account/create')
        self.client.implicitly_wait(10)
        self.client.find_element_by_name('email').send_keys(self.username)
        self.client.find_element_by_name('password').send_keys('password1234')
        self.client.find_element_by_id('joinnow').click()

    def _logout(self):
        self.client.get('https://www.sportpursuit-stage.com/customer/account/logout/')
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//h2[text()="Hello, Welcome Back"]')), "Customer is logged out")

    def _place_order(self):

        # Signup
        self._signup()

        # Add to basket
        self.client.get('https://www.sportpursuit-stage.com/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuMS5zcG9ydHB1cnN1aXQtdWF0LmNvbS9jYXRhbG9nL3Byb2R1Y3Qvdmlldy9pZC80OTQ2NDMv/product/494643')

        # Checkout
        self.client.get('https://www.sportpursuit-stage.com/checkout/prime/')

        # enter delivery info
        self.client.find_element_by_id('shipping:firstname').send_keys('Test')
        self.client.find_element_by_id('shipping:lastname').send_keys('Test')
        self.client.find_element_by_id('shipping:postcode').send_keys('SW12 9ER')
        self.client.find_element_by_id('shipping:street1').send_keys('Test')
        self.client.find_element_by_id('shipping:city').send_keys('Test')
        self.client.find_element_by_id('shipping:telephone').send_keys('123123123')

        # click 'calculate shipping'
        self.client.find_element_by_xpath('//span[text()="Continue to payment"]').click()
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//label[@for="s_method_tablerate_bestway"]')), "Shipping cost is visible")

        # click 'continue to payment'
        self.client.find_element_by_xpath('//span[text()="Continue to payment"]').click()
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//h2[text()="Payment Method"]')), "Payment page visible")

        # enter payment info
        self.client.switch_to.frame(self.client.find_element_by_id('braintree-hosted-field-number'))
        self.client.find_element_by_id('credit-card-number').send_keys('4111111111111111')
        self.client.switch_to.default_content()

        self.client.switch_to.frame(self.client.find_element_by_id('braintree-hosted-field-expirationMonth'))
        self.client.find_element_by_id('expiration-month').send_keys('02')
        self.client.switch_to.default_content()

        self.client.switch_to.frame(self.client.find_element_by_id('braintree-hosted-field-expirationYear'))
        self.client.find_element_by_id('expiration-year').send_keys('20')
        self.client.switch_to.default_content()

        self.client.switch_to.frame(self.client.find_element_by_id('braintree-hosted-field-cvv'))
        self.client.find_element_by_id('cvv').send_keys('123')
        self.client.switch_to.default_content()

        # click place order
        self.client.find_element_by_xpath('//button[contains(@class, "btn-place-order")]/span/span').click()
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "success-order")]')), "Order success popup is visible")

        # Logout
        self._logout()

    def _generate_test_email_address(self):
        return 'webtest-%s@sportpursuit.co.uk' % str(time.time())

    @task(1)
    def shop(self):
        self.client.timed_event_for_locust("", "Place order", self._place_order)


#class LocustUser(PhantomJSLocust):
class LocustUser(FirefoxLocust):

    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior
