from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from pymongo import MongoClient

login = 'study.ai_172@mail.ru'
password = 'NextPassword172#'

def parsmail(driver):
    letter = dict()
    time.sleep(1)

    contact = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(
            (By.CLASS_NAME, 'letter-contact')
        )
    ).get_attribute('title')


    subject = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//h2')
        )
    ).text

    date = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//div[@class="letter__date"]')
        )
    ).text

    body = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(
            (By.CLASS_NAME, 'letter__body')
        )
    ).text

    letter['sender'] = contact
    letter['subject'] = subject
    letter['date'] = date
    letter['body'] = body

    return letter

def main():
    """Entry point."""

    client = MongoClient('localhost', 27017)
    mongo_base = client['mail_db']
    collection = mongo_base['messages']

    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.implicitly_wait(5)

    driver.get('https://account.mail.ru/login')

    login = driver.find_element(By.NAME, 'username')
    login.send_keys('study.ai_172@mail.ru')
    login.send_keys(Keys.ENTER)

    password = driver.find_element(By.NAME, 'password')
    password.send_keys('NextPassword172#')
    password.send_keys(Keys.ENTER)

    first_letter = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.CLASS_NAME, 'js-letter-list-item')
        )
    )
    first_letter.click()

    while True:
        email = parsmail(driver)
        try:
            collection.update_one(email, {'$setOnInsert': email}, upsert=True)

            button_next = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable(
                    (By.CLASS_NAME, 'button2_arrow-down')
                )
            )
            button_next.click()
        except:
            print('All email letters are over')
            break

main()