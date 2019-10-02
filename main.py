import threading

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

class settings():
    url = ''
    sessionid = ''

with open('./src/settings.txt', 'r') as setting:
    setting = setting.readlines()
    settings.url = setting[0][:-1]
    settings.sessionid = setting[1][:-1]

driver = webdriver.Remote(command_executor=settings.url)
driver.close()
driver.session_id = settings.sessionid

driver.get('https://web.whatsapp.com/')

from src.Tools import Tools
Tools = Tools(driver)

def main():
    if '_39gtr' not in driver.find_element_by_xpath('//*[@id="app"]/div').get_attribute('class'):
        # Not logged
        Tools.genQRCODE()
    else:
        # Logged
        Tools.switchContact()

        # The messages will be in this variable
        message = Tools.getLastMessage()[1]

        if message == 'hello':
            Tools.sendMessage('world')
        elif message == '!test':
            Tools.sendMessage('working\n:)')

sleep(5.0)

while True:
    sleep(1)
    main()
