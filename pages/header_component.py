from selenium.webdriver.common.by import By
from .base_page import BasePage

class HeaderComponent(BasePage):
    MEAL_PLAN_LINK = (By.LINK_TEXT, "Meal Plan")
    SHOPPING_LIST_LINK = (By.LINK_TEXT, "Shopping List")
    USER_NAME = (By.CLASS_NAME, "user-name")  # Предполагаемый селектор

    def go_to_meal_plan(self):
        self.click_element(self.MEAL_PLAN_LINK)

    def go_to_shopping_list(self):
        self.click_element(self.SHOPPING_LIST_LINK)

    def is_user_logged_in(self, username):
        return self.is_element_visible(self.USER_NAME) and username in self.get_text(self.USER_NAME)
