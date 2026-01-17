from selenium.webdriver.common.by import By
from .base_page import BasePage

class ShoppingListPage(BasePage):
    SHOPPING_ITEM = (By.CLASS_NAME, "shopping-item")  # Предполагаемый
    CHECKBOX = (By.CLASS_NAME, "item-checkbox")

    def get_items_count(self):
        items = self.driver.find_elements(*self.SHOPPING_ITEM)
        return len(items)

    def mark_item_as_bought(self, index=0):
        checkboxes = self.driver.find_elements(*self.CHECKBOX)
        if checkboxes:
            checkboxes[index].click()

    def is_item_checked(self, index=0):
        checkboxes = self.driver.find_elements(*self.CHECKBOX)
        if checkboxes:
            return checkboxes[index].is_selected()
        return False
