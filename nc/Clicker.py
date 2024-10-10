from os import getenv
from time import sleep
from pathlib import Path

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

URL = 'http://nikifilini.com'
ROULETTE_INITIALIZATION_INTERVAL = 2  # seconds
ROULETTE_SPINNING_INTERVAL = 1  # seconds
EMAIL_INPUT_ACTIVATION_INTERVAL = 1  # seconds
COMPLETION_TIMEOUT = 5  # seconds

TARGETS_PATH = 'assets/targets.py'
EMAIL = getenv('NIKICLICKI_EMAIL')


def get_item_name(item):
    image = item.find_element(by = By.TAG_NAME, value = 'img')
    return Path(image.get_property('src')).stem


def is_better_than(lhs, rhs):
    try:
        lhs_int = int(lhs)
    except ValueError:
        return False

    try:
        rhs_int = int(rhs)
    except ValueError:
        return False

    return lhs_int > rhs_int


class Clicker:
    def __init__(self):
        self.driver = Chrome()

    def reset_driver(self):
        self.driver.quit()
        self.driver = driver = Chrome()

        return driver

    def get_roulette_content(self):
        while True:
            sleep(ROULETTE_INITIALIZATION_INTERVAL)

            try:
                return self.driver.find_element(by = By.CLASS_NAME, value = 'roulette-content')
            except NoSuchElementException:
                pass

    def get_farmed_item(self, roulette_content):
        while True:
            sleep(ROULETTE_SPINNING_INTERVAL)

            try:
                return get_item_name(
                    roulette_content.find_element(by = By.CLASS_NAME, value = 'selected')
                )
            except NoSuchElementException:
                pass

    def list(self):
        driver = self.driver

        driver.get(URL)

        roulette_content = self.get_roulette_content()

        seen_names = set()
        names = []

        for item in roulette_content.find_elements(by = By.CLASS_NAME, value = 'wrap-card'):
            name = get_item_name(item)

            if name in seen_names:
                break

            seen_names.add(name)
            names.append(name)

        with open(TARGETS_PATH, 'w', encoding = 'utf-8') as file:
            file.write('targets = [' + ', '.join(f"'{name}'" for name in names) + ']\n')

    def farm(self, target: str):
        driver = self.driver
        farmed_item_name = None

        while True:
            driver.get(URL)

            roulette_content = self.get_roulette_content()

            submit = roulette_content.find_element(by = By.TAG_NAME, value = 'button')

            submit.click()

            farmed_item_name = self.get_farmed_item(roulette_content)

            # sleep(ROULETTE_SPINNING_TIMEOUT)

            # farmed_item = roulette_content.find_element(by = By.CLASS_NAME, value = 'selected')
            # farmed_item_name = get_item_name(farmed_item)

            if farmed_item_name == target or is_better_than(farmed_item_name, target):
                email = driver.find_element(by = By.XPATH, value = '//input[@type=\'email\']')

                while True:
                    sleep(EMAIL_INPUT_ACTIVATION_INTERVAL)

                    try:
                        email.send_keys(EMAIL)
                        break
                    except ElementNotInteractableException:
                        pass

                driver.find_element(by = By.CLASS_NAME, value = 'send-coupon').click()
                print(f'Successfully rolled \'{farmed_item_name}\'. Exiting...')

                sleep(COMPLETION_TIMEOUT)

                break

            print(f'Rolled \'{farmed_item_name}\', expecting \'{target}\'. Trying again...')
            driver = self.reset_driver()
