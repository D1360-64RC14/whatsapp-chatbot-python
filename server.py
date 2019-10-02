from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from platform import system

chromeOptions = Options()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')

if system() == 'Windows':
    exe = '.exe'
elif system() == 'Linux':
    exe = ''
else:
    print('OS not supported!')
    exit(1)

driver = webdriver.Chrome(f'./src/chromedriver{exe}', options=chromeOptions) # --headless

print(f'URL: {driver.command_executor._url}\nID: {driver.session_id}')
with open('./src/settings.txt', 'w') as settings:
    settings.write(f'{driver.command_executor._url}\n{driver.session_id}\n')
