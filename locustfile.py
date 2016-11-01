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
        self.client.get_screenshot_as_file('screenshot.jpg')
#        self.client.find_element_by_name('email').send_keys(self.username)
#        self.client.find_element_by_name('password').send_keys('password1234')
#        self.client.find_element_by_id('joinnow').click()
#        time.sleep(5)
#        self.client.find_element_by_xpath("//form[@id='form-validate-customer-first-login']/div/input").click()

    def _logout(self):
        self.client.get('https://www.sportpursuit-stage.com/customer/account/logout/')

    def _one_item_checkout(self):
        # Add to basket
        self.client.get('https://www.sportpursuit-stage.com/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuMS5zcG9ydHB1cnN1aXQtdWF0LmNvbS9jYXRhbG9nL3Byb2R1Y3Qvdmlldy9pZC80OTQ2NDMv/product/494643')

        # Checkout
        self.client.get('https://www.sportpursuit-stage.com/checkout/prime/')

        # enter delivery info
        # click 'continue to payment'
        # enter payment info
        # click place order

    def _generate_test_email_address(self):
        return 'webtest-%s@sportpursuit.co.uk' % str(int(time.time()))

    @task(1)
    def shop(self):
        self.client.timed_event_for_locust("", "Signup", self._signup)
        self.client.timed_event_for_locust("", "Order", self._signup)
        self.client.timed_event_for_locust("", "Logout", self._logout)


class LocustUser(PhantomJSLocust):

    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior
