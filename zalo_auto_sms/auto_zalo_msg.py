import getpass
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time

admin_name = getpass.getuser()

class AutoZaloMsg:
    def __init__(self):
        self.driver_path = r"C:\WebDriver\msedgedriver.exe"
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument(fr"user-data-dir=C:\Users\{admin_name}\AppData\Local\Microsoft\Edge\User Data\Profile 1")
        self.options.add_argument("--remote-debugging-port=55219")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-software-rasterizer")
        self.service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 5)
        self.driver_account = ""
        self.sent_status = None
        self.attempt_login = 0
        self.is_logged_in = False
        self.attempt_search = 0

    def open_zalo(self):
        self.driver.get("https://chat.zalo.me/")

    def check_login(self):
        while self.attempt_login < 5 and not self.is_logged_in:
            print(f"Attempt {self.attempt_login + 1}: Checking login status...")
            try:
                qr_code_present = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "qrcode")))

                if qr_code_present:
                    print("QR code still present. Waiting for next attempt...")
                    self.is_logged_in = False
                else:
                    print("QR code disappeared. Login successful.")
                    self.is_logged_in = True
                    break
            except:
                print("QR code not found. Assuming login successful.")
                self.is_logged_in = True
                break  #

            time.sleep(5)
            self.attempt_login += 1

        return self.is_logged_in

    def search_driver(self, driver_phone):
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "contact-search-input")))
        search_box.click()
        search_box.send_keys(Keys.CONTROL + "a")  # Select all text
        search_box.send_keys(Keys.BACKSPACE)
        time.sleep(2)
        search_box.send_keys(driver_phone)

    def has_exist_driver(self):
        try:
            time.sleep(1)
            friend_item = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "gridv2.conv-item.conv-rel")))
        except:
            self.sent_status = 'not found'
            return False
        else:
            friend_item.click()
            return True
        finally:
            self.attempt_search += 1

    def is_new_account(self):
        if self.attempt_search == 0 and self.sent_status == 'not found':
            self.sent_status = 'not found'
            return False
        else:
            element = self.driver.find_element(By.XPATH, "//div-b18[@class='header-title flx flx-al-c flex-1']")
            account_name = element.text
            if account_name != self.driver_account:
                self.driver_account = account_name
                return True
            else:
                self.sent_status = 'duplicated account'
                return False

    def send_message(self, message_lines, will_send):
        for index, line in enumerate(message_lines):
            message_box = self.wait.until(EC.presence_of_element_located((By.ID, f"input_line_{index}")))
            message_box.send_keys(line)
            if index != len(message_lines)-1:
                message_box.send_keys(Keys.SHIFT + Keys.RETURN)
            elif will_send == 'y':
                message_box.send_keys(Keys.RETURN)
        self.sent_status = 'sent'

    def quit(self):
        self.driver.quit()
