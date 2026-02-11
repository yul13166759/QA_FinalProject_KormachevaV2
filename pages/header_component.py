from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from .base_page import BasePage

class HeaderComponent(BasePage):
    # Простые и надежные локаторы для навигации
    MEAL_PLAN_LINK = (By.CSS_SELECTOR, "a[href*='plan']")
    SHOPPING_LIST_LINK = (By.CSS_SELECTOR, "a[href*='shopping']")
    
    USER_NAME = (
        By.XPATH, 
        "//span[contains(@class, 'user') or contains(@class, 'name') or contains(@class, 'username') or contains(@class, 'email') or " +
        "contains(@data-testid, 'user') or contains(@data-testid, 'name') or contains(@data-testid, 'username') or contains(@data-testid, 'email') or " +
        "contains(text(), '@')] | " +
        "//div[contains(@class, 'user') or contains(@class, 'name') or contains(@class, 'username') or contains(@class, 'email') or " +
        "contains(@data-testid, 'user') or contains(@data-testid, 'name') or contains(@data-testid, 'username') or contains(@data-testid, 'email')] | " +
        "//p[contains(@class, 'user') or contains(@class, 'name') or contains(@class, 'username') or contains(@class, 'email') or " +
        "contains(@data-testid, 'user') or contains(@data-testid, 'name') or contains(@data-testid, 'username') or contains(@data-testid, 'email')]"
    )
    
    # Дополнительные локаторы для отладки
    NAVIGATION_MENU = (By.TAG_NAME, "nav")
    BODY = (By.TAG_NAME, "body")
    HEADER = (By.TAG_NAME, "header")
    NAV = (By.TAG_NAME, "nav")
    ASIDE = (By.TAG_NAME, "aside")

    def go_to_meal_plan(self):
        """Переход к плану питания с улучшенной обработкой"""
        try:
            # Сначала проверяем, что мы на нужной странице
            print(f"Current URL: {self.driver.current_url}")
            
            # Ждем загрузки страницы после входа
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.BODY),
                message="Page body not loaded after login"
            )
            
            # Пытаемся найти элемент несколько раз с паузами
            for attempt in range(5):
                try:
                    print(f"Attempt {attempt + 1} to find meal plan link")
                    
                    # Ждем появления навигации или хедера
                    try:
                        self.wait.until(EC.presence_of_element_located(self.NAVIGATION_MENU))
                        print("Found navigation menu")
                    except:
                        try:
                            self.wait.until(EC.presence_of_element_located(self.HEADER))
                            print("Found header")
                        except:
                            try:
                                self.wait.until(EC.presence_of_element_located(self.ASIDE))
                                print("Found aside")
                            except:
                                print("No navigation elements found, checking body")
                    
                    # Ищем ссылку
                    meal_plan_link = self.wait.until(
                        EC.element_to_be_clickable(self.MEAL_PLAN_LINK),
                        message=f"Meal plan link not clickable after {self.wait._timeout} seconds"
                    )
                    
                    print(f"Found meal plan link: {meal_plan_link.text}")
                    print(f"Link href: {meal_plan_link.get_attribute('href')}")
                    print(f"Link classes: {meal_plan_link.get_attribute('class')}")
                    
                    # Делаем скриншот перед кликом
                    self.driver.save_screenshot(f"meal_plan_attempt_{attempt + 1}.png")
                    
                    meal_plan_link.click()
                    
                    # Ждем перехода
                    WebDriverWait(self.driver, 10).until(
                        EC.url_contains('/plan') or EC.url_changes(self.driver.current_url),
                        message="URL did not change after clicking meal plan link"
                    )
                    
                    print(f"Successfully navigated to: {self.driver.current_url}")
                    return
                    
                except TimeoutException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < 4:
                        time.sleep(3)  # Пауза между попытками
                        self.driver.refresh()  # Обновляем страницу
                        # Ждем повторной загрузки
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(self.BODY)
                        )
                    else:
                        # Если все попытки не удалась, попробуем найти все ссылки на странице
                        print("All attempts failed, trying to find all links on page")
                        all_links = self.driver.find_elements(By.TAG_NAME, "a")
                        print(f"Found {len(all_links)} links on page:")
                        for i, link in enumerate(all_links):
                            href = link.get_attribute('href')
                            text = link.text
                            classes = link.get_attribute('class')
                            print(f"  {i+1}. Text: '{text}', Href: '{href}', Classes: '{classes}'")
                        
                        raise
            
        except Exception as e:
            print(f"Error in go_to_meal_plan: {e}")
            # Делаем скриншот для отладки
            self.driver.save_screenshot("debug_meal_plan_final.png")
            raise

    def go_to_shopping_list(self):
        """Переход к списку покупок с улучшенной обработкой"""
        try:
            print(f"Current URL: {self.driver.current_url}")
            
            # Ждем загрузки страницы
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.BODY),
                message="Page body not loaded"
            )
            
            for attempt in range(5):
                try:
                    print(f"Attempt {attempt + 1} to find shopping list link")
                    
                    # Ждем появления навигации
                    try:
                        self.wait.until(EC.presence_of_element_located(self.NAVIGATION_MENU))
                    except:
                        try:
                            self.wait.until(EC.presence_of_element_located(self.HEADER))
                        except:
                            try:
                                self.wait.until(EC.presence_of_element_located(self.ASIDE))
                            except:
                                print("No navigation elements found")
                    
                    # Ищем ссылку
                    shopping_link = self.wait.until(
                        EC.element_to_be_clickable(self.SHOPPING_LIST_LINK),
                        message=f"Shopping list link not clickable after {self.wait._timeout} seconds"
                    )
                    
                    print(f"Found shopping list link: {shopping_link.text}")
                    print(f"Link href: {shopping_link.get_attribute('href')}")
                    print(f"Link classes: {shopping_link.get_attribute('class')}")
                    
                    # Делаем скриншот перед кликом
                    self.driver.save_screenshot(f"shopping_list_attempt_{attempt + 1}.png")
                    
                    shopping_link.click()
                    
                    # Ждем перехода
                    WebDriverWait(self.driver, 10).until(
                        EC.url_contains('/shopping') or EC.url_changes(self.driver.current_url),
                        message="URL did not change after clicking shopping list link"
                    )
                    
                    print(f"Successfully navigated to: {self.driver.current_url}")
                    return
                    
                except TimeoutException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < 4:
                        time.sleep(3)
                        self.driver.refresh()
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(self.BODY)
                        )
                    else:
                        # Если все попытки не удалась, попробуем найти все ссылки на странице
                        print("All attempts failed, trying to find all links on page")
                        all_links = self.driver.find_elements(By.TAG_NAME, "a")
                        print(f"Found {len(all_links)} links on page:")
                        for i, link in enumerate(all_links):
                            href = link.get_attribute('href')
                            text = link.text
                            classes = link.get_attribute('class')
                            print(f"  {i+1}. Text: '{text}', Href: '{href}', Classes: '{classes}'")
                        
                        raise
            
        except Exception as e:
            print(f"Error in go_to_shopping_list: {e}")
            self.driver.save_screenshot("debug_shopping_list_final.png")
            raise

    def is_user_logged_in(self, username):
        """Проверка авторизации пользователя"""
        try:
            # Ждем появления элемента с именем пользователя
            user_element = self.wait.until(
                EC.presence_of_element_located(self.USER_NAME),
                message=f"User name element not found after {self.wait._timeout} seconds"
            )
            
            user_text = user_element.text
            print(f"Found user text: {user_text}")
            
            return username in user_text
            
        except TimeoutException:
            print("User name element not found")
            # Попробуем найти все возможные элементы с пользовательской информацией
            possible_user_elements = self.driver.find_elements(By.XPATH, "//span | //div | //p | //a")
            print("Possible user elements found:")
            for i, element in enumerate(possible_user_elements[:10]):  # Показываем первые 10
                text = element.text
                if text and len(text.strip()) > 0:
                    print(f"  {i+1}. Text: '{text}', Tag: {element.tag_name}")
            
            return False
        except Exception as e:
            print(f"Error checking user login: {e}")
            return False
