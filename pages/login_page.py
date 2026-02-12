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
            current_url = self.driver.current_url
            
            # Ждем загрузки формы
            try:
                form = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(self.FORM),
                    message="Login form not found"
                )
                print(f"Found login form: {form.tag_name}")
            except TimeoutException:
                print("Form not found, checking body content")
                body_text = self.driver.find_element(*self.BODY).text
                print(f"Body text: {body_text[:500]}...")
                raise
            
            # Заполняем поля
            print("Filling username field")
            username_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.USERNAME_FIELD),
                message="Username field not clickable"
            )
            username_field.clear()
            username_field.send_keys(username)
            
            print("Filling password field")
            password_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.PASSWORD_FIELD),
                message="Password field not clickable"
            )
            password_field.clear()
            password_field.send_keys(password)
            
            # Кликаем на кнопку входа
            print("Clicking login button")
            login_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON),
                message="Login button not clickable"
            )
            
            # Делаем скриншот перед кликом
            self.driver.save_screenshot("before_login_click.png")
            
            login_button.click()
            
            # Ждем либо изменения URL, либо появления элемента на главной странице
            print("Waiting for login to complete...")
            try:
                # Пробуем ждать изменения URL
                WebDriverWait(self.driver, 20).until(
                    EC.url_changes(current_url),
                    message="URL did not change after login"
                )
                print(f"URL changed to: {self.driver.current_url}")
            except TimeoutException:
                # Если URL не изменился, проверяем, может быть мы уже на главной
                current_url_after = self.driver.current_url
                print(f"URL after click: {current_url_after}")
                
                # Проверяем наличие элемента, который есть только у авторизованных пользователей
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar, .sidebar, .user-menu")),
                        message="No authenticated user elements found"
                    )
                    print("Found authenticated user elements, login successful")
                except TimeoutException:
                    # Проверяем наличие сообщения об ошибке
                    try:
                        error_msg = self.driver.find_element(By.CSS_SELECTOR, ".alert, .error-message, .form-error").text
                        print(f"Login error message found: {error_msg}")
                    except:
                        pass
                    
                    # Делаем скриншот для отладки
                    self.driver.save_screenshot("login_error.png")
                    raise TimeoutException(f"Login failed - URL did not change from {current_url}")
            
            print(f"Login successful, new URL: {self.driver.current_url}")
            
        except Exception as e:
            print(f"Error during login: {e}")
            # Делаем скриншот для отладки
            try:
                self.driver.save_screenshot("login_error.png")
            except:
                pass
            raise
