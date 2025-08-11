import time
from selenium.webdriver.common.by import By

import config
from selenium import webdriver


def scrape_profile_skills(driver, PROFILE_URL):
    driver.maximize_window()
    driver.get(PROFILE_URL)
    time.sleep(5)
    profile = driver.page_source

    with open(config.RAW_DATA_PATH + 'profile.html', 'w', encoding='utf-8') as f:
        f.write(profile)

    elements = driver.find_elements(By.CLASS_NAME, 'pvs-navigation__text')

    for ele in elements:
        content = str(ele.text)
        if content.__contains__('skills'):
            ele.click()
            break
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)
    skills = driver.page_source
    with open(config.RAW_DATA_PATH + 'skills.html', 'w', encoding='utf-8') as f:
        f.write(skills)
