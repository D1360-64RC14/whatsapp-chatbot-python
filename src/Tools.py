from selenium.common.exceptions import NoSuchElementException
from base64 import b64decode
from PIL import Image
from io import BytesIO
from time import sleep
from os import remove as removeFile

with open('./contactName.txt', 'r') as readContact:
    contactName = readContact.read()

class Tools():
    def __init__(self, driver):
        self.driver = driver
        self.lastMessage = ''

    def genQRCODE(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div/div/div[1][@class="_2Vo52"]')
            print('WhatsApp Web is already opened in another window!')
            exit(1)
        except NoSuchElementException:
            pass

        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/span/div').click()
            sleep(1)
        except:
            pass

        try:
            base64Image = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/img').get_attribute('src')[22:]
        except NoSuchElementException:
            return None

        wt = Image.open('./src/whatsapp.png')
        qrcode = Image.open(BytesIO(b64decode(base64Image)))
        qrcode.paste(wt, (tuple(map((lambda x, y: (x - y) // 2), qrcode.size, wt.size))), wt)

        image = Image.new('RGB', tuple(map(lambda x: x + 80, qrcode.size)), '#ffffff')

        image.paste(qrcode, (tuple(map((lambda x, y: (x - y) // 2), image.size, qrcode.size))))

        image.save('./QR-Code.png')
        print('Read the QR Code in "QR-Code.png"!')

    def switchContact(self):
        try:
            try:
                if self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').text == contactName:
                    return None
            except NoSuchElementException:
                pass

            self.driver.find_element_by_xpath(f'//*[@title="{contactName}"]').click()
            print(f'Connected to: "{contactName}"')
            try:
                removeFile('./QR-Code.png')
            except:
                pass

        except NoSuchElementException:
            print("Contact doesn't exist!")
            exit(1)

    def getLastMessage(self):
        try:
            path = '//*[@id="main"]/div[3]/div/div/div[@class="_1ays2"]/div[last()and@class="FTBzM"][last()]/div/div/div/div[@class="copyable-text" or @class="woe4f copyable-text"]'
            user = self.driver.find_element_by_xpath(path).get_attribute('data-pre-plain-text')[:-2]
            message = self.driver.find_element_by_xpath(f'{path}/div/span/span').text
        except NoSuchElementException:
            return ['', '']

        if self.lastMessage != f'{user}: {message}':
            printMessage = message.replace('\n', f'\n{"-" * len(user)}: ')
            print(f'{user}: {printMessage}')
            self.lastMessage = f'{user}: {message}'
            return [user, message]
        return ['', '']

    def sendMessage(self, message):
        message = message.replace('\n', '\ue008\ue007')
        self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div').send_keys(message)
        self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click()
