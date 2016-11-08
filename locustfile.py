import requests
import random
import time

from realbrowserlocusts import PhantomJSLocust, FirefoxLocust

from locust import TaskSet, task
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LocustUserBehavior(TaskSet):

    base_url = 'https://wws.sportpursuit-stage.com'

    def _signup(self):

        self.client.get(self.base_url + '/customer/account/create')

        self.client.find_element_by_name('email').send_keys(self._generate_test_email_address())
        self.client.find_element_by_name('password').send_keys('password1234')
        self.client.find_element_by_id('joinnow').click()

        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//h2[text()="Congratulations on joining SportPursuit"]')), "Welcome popup not found")

    def _place_order(self):

        # Restart the browser
        self.client.restart()

        # Set implicit wait 
        self.client.implicitly_wait(10)

        # Signup
        self._signup()

        # Add to basket
        self.client.get(self.base_url + '/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuMS5zcG9ydHB1cnN1aXQtdWF0LmNvbS9jYXRhbG9nL3Byb2R1Y3Qvdmlldy9pZC80OTQ2NDMv/product/494643')

        # Checkout
        self.client.get(self.base_url + '/checkout/prime/')

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

    def _generate_test_email_address(self):
        return 'webtest-%s@sportpursuit.co.uk' % str(time.time())

    @task(1)
    def shop(self):
        self.client.timed_event_for_locust("", "Place order", self._place_order)

        self.client.restart_client()


#class LocustUser(PhantomJSLocust):
class LocustUser(FirefoxLocust):

    headless = False
    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior
    headless = False
