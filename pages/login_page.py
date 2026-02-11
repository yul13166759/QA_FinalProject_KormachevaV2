import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class LoginPage(BasePage):
    # Используем правильные селекторы для allauth формы
    USERNAME_FIELD = (By.CSS_SELECTOR, "input[name='login']")  # allauth использует 'login' вместо 'username'
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
    
    # Дополнительные локаторы для отладки
    FORM = (By.TAG_NAME, "form")
    BODY = (By.TAG_NAME, "body")

    def login(self, username, password):
        """Улучшенный метод входа с обработкой ошибок"""
        try:
            print(f"Current URL before login: {self.driver.current_url}")
            
            # Ждем загрузки формы
            try:
                form = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.FORM),
                    message="Login form not found"
                )
                print(f"Found login form: {form.tag_name}")
            except TimeoutException:
                print("Form not found, checking body content")
                body_text = self.driver.find_element(*self.BODY).text
                print(f"Body text: {body_text[:200]}...")
                raise
            
            # Заполняем поля
            print("Filling username field")
            username_field = self.wait.until(
                EC.element_to_be_clickable(self.USERNAME_FIELD),
                message="Username field not clickable"
            )
            username_field.clear()
            username_field.send_keys(username)
            
            print("Filling password field")
            password_field = self.wait.until(
                EC.element_to_be_clickable(self.PASSWORD_FIELD),
                message="Password field not clickable"
            )
            password_field.clear()
            password_field.send_keys(password)
            
            # Кликаем на кнопку входа
            print("Clicking login button")
            login_button = self.wait.until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON),
                message="Login button not clickable"
            )
            
            # Делаем скриншот перед кликом
            self.driver.save_screenshot("before_login_click.png")
            
            login_button.click()
            
            # Ждем перехода после входа
            WebDriverWait(self.driver, 15).until(
                EC.url_changes(self.driver.current_url),
                message="URL did not change after login"
            )
            
            print(f"Login successful, new URL: {self.driver.current_url}")
            
        except Exception as e:
            print(f"Error during login: {e}")
            # Делаем скриншот для отладки
            self.driver.save_screenshot("login_error.png")
            raise
