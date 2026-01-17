from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "id_username")  # Предполагаемые селекторы
    PASSWORD_FIELD = (By.ID, "id_password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, username, password):
        self.fill_field(self.USERNAME_FIELD, username)
        self.fill_field(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)
