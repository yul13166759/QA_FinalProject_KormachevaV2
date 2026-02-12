#!/usr/bin/env python3
"""
Мок-сервер для Tandoor API и UI.
Запускается локально и имитирует ответы реального сервера.
"""

from flask import Flask, jsonify, request, render_template_string
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# Хранилище данных
recipes = [
    {"id": 1, "name": "Омлет с сыром", "servings": 2},
    {"id": 2, "name": "Куриный суп", "servings": 4},
]

meal_plans = []
shopping_list = []

# ========== API Endpoints ==========

@app.route('/api/recipe/', methods=['GET'])
def get_recipes():
    """Получить список рецептов"""
    return jsonify({"results": recipes, "count": len(recipes)})

@app.route('/api/meal-plan/', methods=['GET'])
def get_meal_plans():
    """Получить список планов питания"""
    return jsonify({"results": meal_plans, "count": len(meal_plans)})

@app.route('/api/meal-plan/', methods=['POST'])
def create_meal_plan():
    """Создать план питания"""
    data = request.json
    plan = {
        "id": len(meal_plans) + 1,
        "title": data.get("title", "New Plan"),
        "from_date": data.get("from_date"),
        "to_date": data.get("to_date"),
        "meal_type": data.get("meal_type", "Dinner"),
        "recipe": data.get("recipe"),
        "servings": data.get("servings", 2),
        "add_to_shopping": data.get("add_to_shopping", False),
        "created_at": datetime.now().isoformat()
    }
    meal_plans.append(plan)
    
    # Если нужно добавить в список покупок
    if plan["add_to_shopping"]:
        shopping_list.append({
            "id": len(shopping_list) + 1,
            "name": f"Ingredients for {plan['title']}",
            "checked": False
        })
    
    return jsonify(plan), 201

@app.route('/api/meal-plan/<int:plan_id>/', methods=['DELETE'])
def delete_meal_plan(plan_id):
    """Удалить план питания"""
    global meal_plans
    meal_plans = [p for p in meal_plans if p["id"] != plan_id]
    return jsonify({"message": "Deleted"}), 204

@app.route('/api/shopping-list/', methods=['GET'])
def get_shopping_list():
    """Получить список покупок"""
    return jsonify({"results": shopping_list, "count": len(shopping_list)})

# ========== UI Pages ==========

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - Tandoor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; }
        input { width: 100%; padding: 10px; margin: 10px 0; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Login to Tandoor</h1>
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST" action="/accounts/login/">
        <input type="text" name="login" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

MEAL_PLAN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Meal Plan - Tandoor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        nav { background: #f8f9fa; padding: 10px; margin-bottom: 20px; }
        nav a { margin-right: 20px; text-decoration: none; color: #007bff; }
        .plan-item { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; }
        .delete-btn { background: #dc3545; }
        form { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
        input, select { padding: 8px; margin: 5px; }
    </style>
</head>
<body>
    <nav>
        <a href="/plan/">Meal Plan</a>
        <a href="/shopping/">Shopping List</a>
        <span style="float:right;">Welcome, admin!</span>
    </nav>
    
    <h1>Meal Plans</h1>
    
    <form method="POST" action="/plan/create/">
        <h3>Create New Plan</h3>
        <input type="text" name="title" placeholder="Plan Title" required>
        <input type="date" name="from_date" required>
        <input type="date" name="to_date" required>
        <select name="meal_type">
            <option value="Breakfast">Breakfast</option>
            <option value="Lunch">Lunch</option>
            <option value="Dinner" selected>Dinner</option>
        </select>
        <select name="recipe">
            {% for recipe in recipes %}
            <option value="{{ recipe.id }}">{{ recipe.name }}</option>
            {% endfor %}
        </select>
        <input type="number" name="servings" value="2" min="1">
        <label><input type="checkbox" name="add_to_list"> Add to shopping list</label>
        <br><br>
        <button type="submit">Create Plan</button>
    </form>
    
    <h3>Your Plans:</h3>
    {% for plan in plans %}
    <div class="plan-item">
        <h4>{{ plan.title }}</h4>
        <p>From: {{ plan.from_date }} To: {{ plan.to_date }}</p>
        <p>Type: {{ plan.meal_type }} | Servings: {{ plan.servings }}</p>
        <form method="POST" action="/plan/delete/{{ plan.id }}/" style="display:inline;">
            <button type="submit" class="delete-btn">Delete</button>
        </form>
    </div>
    {% else %}
    <p>No meal plans yet.</p>
    {% endfor %}
</body>
</html>
"""

SHOPPING_LIST_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Shopping List - Tandoor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        nav { background: #f8f9fa; padding: 10px; margin-bottom: 20px; }
        nav a { margin-right: 20px; text-decoration: none; color: #007bff; }
        .item { border: 1px solid #ddd; padding: 10px; margin: 5px 0; }
        .checked { text-decoration: line-through; color: #888; }
    </style>
</head>
<body>
    <nav>
        <a href="/plan/">Meal Plan</a>
        <a href="/shopping/">Shopping List</a>
        <span style="float:right;">Welcome, admin!</span>
    </nav>
    
    <h1>Shopping List</h1>
    <p>Items: {{ items|length }}</p>
    
    {% for item in items %}
    <div class="item {% if item.checked %}checked{% endif %}">
        <form method="POST" action="/shopping/toggle/{{ item.id }}/" style="display:inline;">
            <input type="checkbox" {% if item.checked %}checked{% endif %} onChange="this.form.submit()">
            {{ item.name }}
        </form>
    </div>
    {% else %}
    <p>Your shopping list is empty.</p>
    {% endfor %}
</body>
</html>
"""

@app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Страница логина"""
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        # Принимаем любые учетные данные для тестирования
        if username and password:
            return "<script>window.location.href='/plan/';</script>"
        return render_template_string(LOGIN_PAGE, error="Invalid credentials")
    return render_template_string(LOGIN_PAGE, error=None)

@app.route('/plan/')
def meal_plan_page():
    """Страница планов питания"""
    return render_template_string(MEAL_PLAN_PAGE, plans=meal_plans, recipes=recipes)

@app.route('/plan/create/', methods=['POST'])
def create_plan_form():
    """Создание плана через форму"""
    plan = {
        "id": len(meal_plans) + 1,
        "title": request.form.get("title"),
        "from_date": request.form.get("from_date"),
        "to_date": request.form.get("to_date"),
        "meal_type": request.form.get("meal_type"),
        "recipe": request.form.get("recipe"),
        "servings": int(request.form.get("servings", 2)),
        "add_to_shopping": "add_to_list" in request.form
    }
    meal_plans.append(plan)
    
    if plan["add_to_shopping"]:
        shopping_list.append({
            "id": len(shopping_list) + 1,
            "name": f"Ingredients for {plan['title']}",
            "checked": False
        })
    
    return "<script>window.location.href='/plan/';</script>"

@app.route('/plan/delete/<int:plan_id>/', methods=['POST'])
def delete_plan_form(plan_id):
    """Удаление плана через форму"""
    global meal_plans
    meal_plans = [p for p in meal_plans if p["id"] != plan_id]
    return "<script>window.location.href='/plan/';</script>"

@app.route('/shopping/')
def shopping_list_page():
    """Страница списка покупок"""
    return render_template_string(SHOPPING_LIST_PAGE, items=shopping_list)

@app.route('/shopping/toggle/<int:item_id>/', methods=['POST'])
def toggle_shopping_item(item_id):
    """Отметить элемент как купленный"""
    for item in shopping_list:
        if item["id"] == item_id:
            item["checked"] = not item.get("checked", False)
            break
    return "<script>window.location.href='/shopping/';</script>"

@app.route('/')
def index():
    """Главная страница - редирект на логин"""
    return "<script>window.location.href='/accounts/login/';</script>"

if __name__ == '__main__':
    print("="*60)
    print("🚀 Запуск мок-сервера Tandoor")
    print("="*60)
    print("\n📍 URL для тестов:")
    print("   - UI: http://localhost:8000")
    print("   - API: http://localhost:8000/api/")
    print("\n👤 Логин: любой username/password")
    print("\n⛔ Для остановки нажмите Ctrl+C")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=8000, debug=False)
