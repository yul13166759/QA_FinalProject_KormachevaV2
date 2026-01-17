import json
import datetime
from api.client import TandoorAPIClient

def generate_test_data():
    client = TandoorAPIClient()

    # Загрузить ссылки из файла
    with open('test_data.json', 'r') as f:
        recipe_urls = json.load(f)

    recipes = []
    for url in recipe_urls:
        recipe = client.import_recipe(url)
        if recipe:
            recipes.append(recipe['id'])

    # Создать данные для плана питания
    today = datetime.date.today()
    plan_data = {
        "title": "Test Meal Plan",
        "recipe": recipes[0] if recipes else None,
        "from_date": str(today),
        "to_date": str(today + datetime.timedelta(days=7)),
        "meal_type": "Завтрак",
        "servings": 2
    }

    return plan_data

if __name__ == "__main__":
    data = generate_test_data()
    print("Generated test data:", data)
