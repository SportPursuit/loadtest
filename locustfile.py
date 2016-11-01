import requests
import random

from realbrowserlocusts import PhantomJSLocust

from locust import TaskSet, task


class LocustUserBehavior(TaskSet):

    def _login(self):
        self.username = requests.get('http://127.0.0.1:5000/').text
        self.client.implicitly_wait(30)
        self.client.get('https://www.sportpursuit-stage.com/customer/account/login')
        self.client.find_element_by_name('login[username]').send_keys(self.username)
        self.client.find_element_by_name('login[password]').send_keys('password1234')
        self.client.find_element_by_name('send').click()

    def _logout(self):
        requests.get('http://127.0.0.1:5000/%s' % self.username)
        self.client.get('https://www.sportpursuit-stage.com/customer/account/logout/')

    def _one_item_checkout(self):
        self.client.get('https://www.sportpursuit-stage.com/')
        sales = self.client.find_elements_by_class_name('sale')
        random.choice(sales).click()


    def _two_item_checkout(self):
        self.client.get('https://www.sportpursuit-stage.com/')
        sales = self.client.find_elements_by_class_name('sale')
        random.choice(sales).click()

    @task(1)
    def shop(self):
        self.client.timed_event_for_locust("", "Login", self._login)

        try:
            event = random.choice([
                ("", "One Item Checkout", self._one_item_checkout),
                ("", "Two Item Checkout", self._two_item_checkout)
            ])

            self.client.timed_event_for_locust(*event)
        except:
            raise
        finally:
            self.client.timed_event_for_locust("", "Logout", self._logout)


class LocustUser(PhantomJSLocust):

    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior