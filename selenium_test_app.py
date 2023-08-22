import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):

    # initialization of webdriver
    def setUp(self):
        self.driver = webdriver.Chrome()

    # Test case method. It should always start with test_
    def test_search_in_timesheet(self):
        driver = self.driver
        timesheet_url = os.getenv("TIMESHEET_URL")
        driver.get(timesheet_url)
        username_field = driver.find_element(By.NAME, "login")
        password_field = driver.find_element(By.NAME, "password")
        user_name = os.getenv("USER_NAME")
        password = os.getenv("PASSWORD")
        username_field.send_keys(user_name)
        password_field.send_keys(password)
        time.sleep(2)
        password_field.send_keys(Keys.RETURN)
        current_url = driver.current_url
        expected_home_url = os.getenv("TIMESHEET_HOME_URL")
        assert current_url == expected_home_url
        absent_calendar_link = driver.find_elements("xpath", '//li[@id="iconcolor"]')[1]
        time.sleep(2)
        absent_calendar_link.click()
        time.sleep(2)
        current_url = driver.current_url
        expected_absent_url = os.getenv("ABSENT_URL")
        assert current_url == expected_absent_url
        office_hours_url = os.getenv("OFFICE_HOURS_URL")
        office_hours_link = driver.find_element("xpath", '//*[@id="side-main-menu"]/li[4]')
        time.sleep(2)
        office_hours_link.click()
        time.sleep(2)
        current_url = driver.current_url
        assert current_url == office_hours_url

    # cleanup method called after every test performed
    def tearDown(self):
        self.driver.close()


# execute the script
if __name__ == "__main__":
    unittest.main()
