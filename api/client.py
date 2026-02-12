import requests
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

class TandoorAPIClient:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.token = os.getenv('TANDOOR_TOKEN')
        self.username = os.getenv('TANDOOR_USERNAME')
        self.password = os.getenv('TANDOOR_PASSWORD')
        
        # Создаем сессию с retry стратегией
        self.session = requests.Session()
        
        # Retry strategy для повторных попыток
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Заголовки
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        # Добавляем токен если есть
        if self.token:
            self.headers['Authorization'] = f'Token {self.token}'
        
        self.session.headers.update(self.headers)
        
        # Базовая авторизация
        self.auth = HTTPBasicAuth(self.username, self.password) if self.username and self.password else None
        
        # Таймаут для запросов
        self.timeout = 60
    
    def _make_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(
                method, 
                url, 
                json=data, 
                params=params,
                auth=self.auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print(f"Error: Request timeout for {url} - проверьте VPN")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Error: Connection error for {url} - возможно, нужен VPN")
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print(f"Error 403 Forbidden: {e} - Недостаточно прав")
            else:
                print(f"HTTP Error {response.status_code}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def import_recipe(self, url):
        data = {"url": url}
        response = self._make_request('POST', '/api/bookmarklet/import/', data)
        if response:
            return self._safe_json_parse(response)
        return None

    def get_recipes(self):
        response = self._make_request('GET', '/api/recipe/')
        if response:
            return self._safe_json_parse(response)
        return None

    def get_recipe(self, recipe_id):
        """Получить рецепт по ID"""
        response = self._make_request('GET', f'/api/recipe/{recipe_id}/')
        if response:
            return self._safe_json_parse(response)
        return None

    def delete_recipe(self, recipe_id):
        response = self._make_request('DELETE', f'/api/recipe/{recipe_id}/')
        return response is not None

    def create_meal_plan(self, data):
        response = self._make_request('POST', '/api/plan/', data)
        if response:
            return self._safe_json_parse(response)
        return None

    def get_meal_plan(self, plan_id):
        response = self._make_request('GET', f'/api/plan/{plan_id}/')
        if response:
            return self._safe_json_parse(response)
        return None

    def delete_meal_plan(self, plan_id):
        response = self._make_request('DELETE', f'/api/plan/{plan_id}/')
        return response is not None

    def get_shopping_list(self):
        response = self._make_request('GET', '/api/shopping-list/')
        if response:
            return self._safe_json_parse(response)
        return None

    def _safe_json_parse(self, response):
        """Безопасный парсинг JSON с проверкой content-type"""
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            try:
                return response.json()
            except ValueError:
                print(f"Error: Invalid JSON response from {response.url}")
                return None
        else:
            print(f"Error: Expected JSON but got {content_type} from {response.url}")
            return None

    def test_connection(self):
        recipes = self.get_recipes()
        if recipes:
            print("Connection successful. Recipes:", recipes)
        else:
            print("Connection failed.")

if __name__ == "__main__":
    client = TandoorAPIClient()
    client.test_connection()
