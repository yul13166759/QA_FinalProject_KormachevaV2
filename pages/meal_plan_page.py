from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class MealPlanPage(BasePage):
    # Кнопки
    CREATE_BUTTON = (By.CSS_SELECTOR, "button.v-btn.text-save .v-btn__content")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'text-save')]//span[contains(text(), 'Создать')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(@class, 'text-delete')]//span[contains(text(), 'Удалить')]")
    
    # Поля формы (по placeholder и структуре Vuetify)
    RECIPE_FIELD = (By.CSS_SELECTOR, "input[placeholder='Рецепт']")
    PLAN_TITLE_FIELD = (By.CSS_SELECTOR, "input[id^='input-v-'][type='text']")
    DATE_FIELD = (By.CSS_SELECTOR, "input[placeholder='dd.mm.yyyy']")
    MEAL_TYPE_FIELD = (By.CSS_SELECTOR, ".multiselect-single-label-text")  # Выбранное значение
    SERVINGS_FIELD = (By.CSS_SELECTOR, "input[id^='input-v-'][inputmode='decimal']")
    
    # Элементы списка
    PLAN_ITEM = (By.CSS_SELECTOR, ".v-card, .meal-plan-item")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".v-snackbar__content, .alert-success")

    def create_plan(self, title, from_date, to_date, meal_type, recipe, servings, add_to_list=False):
        """Создание плана питания с учетом Vuetify компонентов"""
        # Клик по кнопке Создать
        self.click_element(self.CREATE_BUTTON)
        
        # Ждем появления модального окна/формы
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.RECIPE_FIELD)
        )
        
        # Заполняем поля
        self.fill_field(self.RECIPE_FIELD, recipe)
        self.fill_field(self.PLAN_TITLE_FIELD, title)
        
        # Дата - очищаем и заполняем
        date_field = self.driver.find_element(*self.DATE_FIELD)
        date_field.clear()
        date_field.send_keys(f"{from_date} - {to_date}")
        
        # Порции
        servings_field = self.driver.find_element(*self.SERVINGS_FIELD)
        servings_field.clear()
        servings_field.send_keys(str(servings))
        
        # Клик по кнопке Сохранить
        self.click_element(self.SAVE_BUTTON)
        
        # Ждем закрытия формы или появления сообщения об успехе
        WebDriverWait(self.driver, 10).until(
            EC.any_of(
                EC.invisibility_of_element_located(self.RECIPE_FIELD),
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
        )

    def is_plan_created(self, title):
        """Проверка создания плана по заголовку"""
        try:
            plan_locator = (By.XPATH, f"//*[contains(text(), '{title}')]")
            return self.is_element_visible(plan_locator)
        except:
            return False

    def delete_plan(self, title):
        """Удаление плана по заголовку"""
        # Найти план и кликнуть кнопку удаления
        plan_row = (By.XPATH, f"//*[contains(text(), '{title}')]/ancestor::div[contains(@class, 'v-card') or contains(@class, 'meal-plan-item')]")
        
        # Находим план и кликаем удалить внутри него
        plan_element = self.driver.find_element(*plan_row)
        delete_btn = plan_element.find_element(By.XPATH, ".//button[contains(@class, 'text-delete') or contains(., 'Удалить')]")
        delete_btn.click()
        
        # Подтверждение удаления (если есть диалог)
        try:
            confirm_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Да') or contains(., 'Подтвердить')]"))
            )
            confirm_btn.click()
        except:
            pass  # Может не быть подтверждения
