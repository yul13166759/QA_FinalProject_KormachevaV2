from selenium.webdriver.common.by import By
from .base_page import BasePage

class HeaderComponent(BasePage):
    # Используем более надежные локаторы - по href или data-testid
    MEAL_PLAN_LINK = (By.XPATH, "//a[contains(@href, '/plan') or contains(@href, 'meal') or contains(text(), 'Meal')]")
    SHOPPING_LIST_LINK = (By.XPATH, "//a[contains(@href, '/shopping') or contains(text(), 'Shopping')]")
    USER_NAME = (By.XPATH, "//span[contains(@class, 'user') or contains(@class, 'name')] | //div[contains(@class, 'user')]")

    def go_to_meal_plan(self):
        self.click_element(self.MEAL_PLAN_LINK)

    def go_to_shopping_list(self):
        self.click_element(self.SHOPPING_LIST_LINK)

    def is_user_logged_in(self, username):
        return self.is_element_visible(self.USER_NAME) and username in self.get_text(self.USER_NAME)
