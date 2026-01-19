import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.XPATH, "//input[@name='username']")  # Используем XPath для универсальности
    PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    def login(self, username, password):
        time.sleep(5)  # Ждём загрузки страницы
        self.fill_field(self.USERNAME_FIELD, username)
        self.fill_field(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)
