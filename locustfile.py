import requests
import random
import time

from realbrowserlocusts import PhantomJSLocust

from locust import TaskSet, task


class LocustUserBehavior(TaskSet):

    def _signup(self):
        self.username = self._generate_test_email_address() 
        self.client.implicitly_wait(10)
        self.client.get('https://www.sportpursuit-stage.com/customer/account/create')
        self.client.implicitly_wait(10)
        time.sleep(5)
        self.client.find_element_by_name('email').send_keys(self.username)
        self.client.find_element_by_name('password').send_keys('password1234')
        self.client.find_element_by_id('joinnow').click()

    def _logout(self):
        self.client.get('https://www.sportpursuit-stage.com/customer/account/logout/')

    def _checkout(self):
        # Add to basket
        self.client.get('https://www.sportpursuit-stage.com/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuMS5zcG9ydHB1cnN1aXQtdWF0LmNvbS9jYXRhbG9nL3Byb2R1Y3Qvdmlldy9pZC80OTQ2NDMv/product/494643')

        # Checkout
        self.client.get('https://www.sportpursuit-stage.com/checkout/prime/')
        time.sleep(5)

        self.client.save_screenshot('screenshot1.jpg')

        self.client.find_element_by_xpath('//li[@id="opc-shipping-tab"]/div/h2/span').click()

        time.sleep(5)
        self.client.save_screenshot('screenshot2.jpg')

        # enter delivery info
        self.client.find_element_by_id('shipping:firstname').send_keys('Test')
        self.client.find_element_by_id('shipping:lastname').send_keys('Test')
        self.client.find_element_by_id('shipping:country_id').send_keys('Test')
        self.client.find_element_by_id('shipping:street1').send_keys('Test')
        self.client.find_element_by_id('shipping:city').send_keys('Test')
        self.client.find_element_by_id('shipping:telephone').send_keys('123123123')

        self.client.save_screenshot('screenshot3.jpg')

        # click 'continue to payment'
        # enter payment info
        # click place order

    def _generate_test_email_address(self):
        return 'webtest-%s@sportpursuit.co.uk' % str(int(time.time()))

    @task(1)
    def shop(self):
        self.client.timed_event_for_locust("", "Signup", self._signup)
        self.client.timed_event_for_locust("", "Order", self._checkout)
        self.client.timed_event_for_locust("", "Logout", self._logout)


class LocustUser(PhantomJSLocust):

    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior
