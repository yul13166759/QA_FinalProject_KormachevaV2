from selenium.webdriver.common.by import By
from .base_page import BasePage

class MealPlanPage(BasePage):
    CREATE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='create-meal-plan-btn']")
    PLAN_TITLE_FIELD = (By.CSS_SELECTOR, "input[data-testid='meal-plan-title']")
    FROM_DATE_FIELD = (By.CSS_SELECTOR, "input[data-testid='meal-plan-from-date']")
    TO_DATE_FIELD = (By.CSS_SELECTOR, "input[data-testid='meal-plan-to-date']")
    MEAL_TYPE_FIELD = (By.CSS_SELECTOR, "select[data-testid='meal-plan-meal-type']")
    RECIPE_FIELD = (By.CSS_SELECTOR, "select[data-testid='meal-plan-recipe']")
    SERVINGS_FIELD = (By.CSS_SELECTOR, "input[data-testid='meal-plan-servings']")
    ADD_TO_SHOPPING_LIST_CHECKBOX = (By.CSS_SELECTOR, "input[data-testid='add-to-shopping-list']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='save-meal-plan-btn']")
    PLAN_ITEM = (By.CSS_SELECTOR, ".meal-plan-item")  # Более конкретный селектор

    def create_plan(self, title, from_date, to_date, meal_type, recipe, servings, add_to_list=False):
        self.click_element(self.CREATE_BUTTON)
        self.fill_field(self.PLAN_TITLE_FIELD, title)
        self.fill_field(self.FROM_DATE_FIELD, from_date)
        self.fill_field(self.TO_DATE_FIELD, to_date)
        self.fill_field(self.MEAL_TYPE_FIELD, meal_type)
        self.fill_field(self.RECIPE_FIELD, recipe)
        self.fill_field(self.SERVINGS_FIELD, str(servings))
        if add_to_list:
            self.click_element(self.ADD_TO_SHOPPING_LIST_CHECKBOX)
        self.click_element(self.SAVE_BUTTON)

    def is_plan_created(self, title):
        return self.is_element_visible((By.XPATH, f"//div[contains(text(), '{title}')]"))

    def delete_plan(self, title):
        # Найти и кликнуть на план, затем удалить
        plan_locator = (By.XPATH, f"//div[contains(text(), '{title}')]/following-sibling::button[text()='Удалить']")
        self.click_element(plan_locator)
