import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

print(f"BASE_URL: {os.getenv('BASE_URL')}")
print(f"TANDOOR_USERNAME: {os.getenv('TANDOOR_USERNAME')}")
token = os.getenv('TANDOOR_TOKEN')
print(f"TANDOOR_TOKEN: {token[:10] if token else 'None'}...")

# Проверяем подключение к API
from api.client import TandoorAPIClient

client = TandoorAPIClient()
print(f"\nClient base_url: {client.base_url}")
print(f"Client token: {client.token[:10] if client.token else 'None'}...")
print(f"Client auth: {client.auth}")

print("\nПопытка получить рецепты...")
recipes = client.get_recipes()
print(f"Recipes: {recipes}")

if recipes:
    print("\n✅ API подключение успешно!")
else:
    print("\n❌ API не доступен или нет данных")
