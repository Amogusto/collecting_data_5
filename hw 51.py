from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service('./cromedriver')
driver = webdriver.Chrome(service=s)
driver.get("https://gb.ru/login")