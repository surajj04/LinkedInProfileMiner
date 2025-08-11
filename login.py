import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config


def linkedin_login():
    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    driver.find_element(By.ID, 'username').send_keys(config.LINKEDIN_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(config.LINKEDIN_PASSWORD)
    driver.find_element(By.ID, 'password').send_keys(Keys.ENTER)
    time.sleep(3)

    return driver
