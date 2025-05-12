import pytest
from src.mealplan import MealPlan
from src.recipe import Recipe


#############################################
# Fixtures #
#############################################

@pytest.fixture
def basic_recipe():
    return Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)


#############################################
# Testy inicjalizacji i podstawowej struktury #
#############################################

def test_mealplan_initialization():
    """Test sprawdzający poprawność inicjalizacji pustego planu posiłków"""
    plan = MealPlan()
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    assert len(plan.plan) == 7
    for day in days:
        assert day in plan.plan
        assert plan.plan[day] == []


#############################################
# Testy dodawania posiłków #
#############################################

def test_mealplan_invalid_recipe_type():
    """Test sprawdzający reakcję na próbę dodania nieprawidłowego typu przepisu"""
    plan = MealPlan()
    with pytest.raises(TypeError):
        plan.add_meal("Monday", "not_a_recipe")


@pytest.mark.parametrize(
    "day",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
)
def test_add_meal_and_summary(basic_recipe, day):
    """Test sprawdzający dodawanie posiłków do każdego dnia tygodnia i poprawność podsumowania"""
    plan = MealPlan()
    plan.add_meal(day, basic_recipe)
    summary = plan.daily_summary(day)
    assert summary["kcal"] == 150
    assert summary["protein"] == 5
    assert summary["fat"] == 2
    assert summary["carbs"] == 20


@pytest.mark.parametrize("invalid_day", ["Funday", "Yesterday", "", None])
def test_invalid_day_meal_add_raises(basic_recipe, invalid_day):
    """Test sprawdzający dodawanie posiłku do nieprawidłowego dnia"""
    plan = MealPlan()
    with pytest.raises(ValueError):
        plan.add_meal(invalid_day, basic_recipe)


@pytest.mark.parametrize("day", ["", None, 123, "NotADay", "monday"])
def test_invalid_day_operations(day):
    """Test różnych nieprawidłowych dni"""
    plan = MealPlan()
    recipe = Recipe("Test", {}, 100, 1, 1, 1)

    with pytest.raises((ValueError, TypeError)):
        plan.add_meal(day, recipe)

    with pytest.raises((ValueError, TypeError)):
        plan.daily_summary(day)


def test_add_multiple_meals_to_same_day():
    """Test sprawdzający dodawanie wielu posiłków do tego samego dnia"""
    mp = MealPlan()
    recipe1 = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
    recipe2 = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)
    recipe3 = Recipe("Dinner", {"chicken": 200}, 300, 30, 10, 0)

    mp.add_meal("Wednesday", recipe1)
    mp.add_meal("Wednesday", recipe2)
    mp.add_meal("Wednesday", recipe3)

    assert len(mp.plan["Wednesday"]) == 3
    summary = mp.daily_summary("Wednesday")
    assert summary["kcal"] == 630
    assert summary["protein"] == 45
    assert summary["fat"] == 21
    assert summary["carbs"] == 35


def test_mealplan_adding_same_recipe_multiple_times():
    """Test sprawdzający wielokrotne dodawanie tego samego przepisu"""
    plan = MealPlan()
    r = Recipe("Repeat", {"x": 1}, 100, 5, 5, 5)
    for _ in range(10):
        plan.add_meal("Friday", r)
    summary = plan.daily_summary("Friday")
    assert summary["kcal"] == 1000
    assert summary["protein"] == 50
    assert summary["fat"] == 50
    assert summary["carbs"] == 50


def test_add_same_recipe_multiple_times():
    """Test sprawdzający wielokrotne dodawanie tego samego obiektu przepisu"""
    mp = MealPlan()
    recipe = Recipe("Snack", {"nuts": 50}, 280, 10, 22, 8)
    mp.add_meal("Monday", recipe)
    mp.add_meal("Monday", recipe)
    assert len(mp.plan["Monday"]) == 2
    assert mp.daily_summary("Monday")["kcal"] == 560


@pytest.mark.parametrize(
    "day,recipes",
    [
        (
            "Monday",
            [
                Recipe("A", {"x": 1}, 100, 10, 5, 5),
                Recipe("B", {"y": 2}, 200, 20, 10, 10),
            ],
        ),
        ("Tuesday", [Recipe("C", {"z": 3}, 150, 15, 7, 7)]),
        (
            "Wednesday",
            [Recipe("D", {"a": 1}, 80, 8, 4, 3), Recipe("E", {"b": 2}, 120, 10, 5, 5)],
        ),
    ],
)
def test_multiple_recipes_daily_summary(day, recipes):
    """Test sprawdzający poprawność sumowania wartości odżywczych dla wielu przepisów"""
    plan = MealPlan()
    for r in recipes:
        plan.add_meal(day, r)
    summary = plan.daily_summary(day)
    assert summary["kcal"] == sum(r.kcal for r in recipes)
    assert summary["protein"] == sum(r.protein for r in recipes)
    assert summary["fat"] == sum(r.fat for r in recipes)
    assert summary["carbs"] == sum(r.carbs for r in recipes)


#############################################
# Testy usuwania posiłków #
#############################################

def test_remove_meal():
    """Test sprawdzający usuwanie posiłku z danego dnia"""
    plan = MealPlan()
    recipe = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)
    plan.add_meal("Monday", recipe)
    plan.remove_meal("Monday", recipe)
    assert len(plan.plan["Monday"]) == 0


def test_remove_non_existent_meal():
    """Test sprawdzający usuwanie nieistniejącego posiłku"""
    plan = MealPlan()
    recipe = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)
    plan.add_meal("Monday", recipe)
    another_recipe = Recipe("Pancake", {"flour": 100}, 200, 6, 8, 30)
    with pytest.raises(ValueError):
        plan.remove_meal("Monday", another_recipe)


def test_remove_meal_from_non_existent_day():
    """Test sprawdzający usuwanie posiłku z nieistniejącego dnia"""
    plan = MealPlan()
    recipe = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)
    with pytest.raises(ValueError):
        plan.remove_meal("NonExistentDay", recipe)


def test_add_and_remove_meals_from_multiple_days():
    """Test sprawdzający dodawanie i usuwanie posiłków z różnych dni"""
    plan = MealPlan()
    recipe1 = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
    recipe2 = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)

    plan.add_meal("Monday", recipe1)
    plan.add_meal("Tuesday", recipe2)
    plan.remove_meal("Monday", recipe1)

    assert len(plan.plan["Monday"]) == 0
    assert len(plan.plan["Tuesday"]) == 1


def test_add_and_remove_meal_multiple_times():
    """Test sprawdzający wielokrotne dodawanie i usuwanie posiłków"""
    plan = MealPlan()
    recipe = Recipe("Snack", {"nuts": 50}, 280, 10, 22, 8)

    plan.add_meal("Monday", recipe)
    plan.add_meal("Monday", recipe)
    plan.remove_meal("Monday", recipe)
    assert len(plan.plan["Monday"]) == 1
    plan.remove_meal("Monday", recipe)
    assert len(plan.plan["Monday"]) == 0


#############################################
# Testy podsumowań #
#############################################

@pytest.mark.parametrize("day", ["Monday", "Tuesday", "Wednesday"])
def test_mealplan_with_empty_day(day):
    """Test sprawdzający podsumowanie dla dni bez żadnych posiłków"""
    plan = MealPlan()
    plan.plan[day] = []  # Jawnie pusto
    assert plan.daily_summary(day) == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}


def test_mealplan_invalid_day_summary():
    """Test sprawdzający próbę pobrania podsumowania dla nieistniejącego dnia"""
    plan = MealPlan()
    with pytest.raises(ValueError):
        plan.daily_summary("NonExistentDay")


def test_weekly_summary():
    """Test sprawdzający metodę weekly_summary"""
    plan = MealPlan()
    recipe1 = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)
    recipe2 = Recipe("Pancake", {"flour": 100}, 200, 6, 8, 30)
    recipe3 = Recipe("Salad", {"lettuce": 50}, 100, 3, 1, 15)

    plan.add_meal("Monday", recipe1)
    plan.add_meal("Tuesday", recipe2)
    plan.add_meal("Wednesday", recipe3)

    summary = plan.weekly_summary()
    assert summary["Monday"]["kcal"] == 150
    assert summary["Tuesday"]["kcal"] == 200
    assert summary["Wednesday"]["kcal"] == 100


def test_weekly_summary_empty_plan():
    """Test sprawdzający metodę weekly_summary dla pustego planu"""
    plan = MealPlan()
    summary = plan.weekly_summary()
    for day in plan.plan.keys():
        assert summary[day]["kcal"] == 0


def test_mealplan_with_partially_filled_week():
    """Test sprawdzający plan z częściowo wypełnionym tygodniem"""
    plan = MealPlan()
    breakfast = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)

    # Dodaj posiłki tylko w niektóre dni
    plan.add_meal("Monday", breakfast)
    plan.add_meal("Wednesday", breakfast)
    plan.add_meal("Friday", breakfast)

    summary = plan.weekly_summary()
    assert summary["Monday"]["kcal"] == 180
    assert summary["Tuesday"]["kcal"] == 0  # Dzień bez posiłków
    assert summary["Wednesday"]["kcal"] == 180


#############################################
# Testy dodatkowych metod #
#############################################

def test_get_meals():
    """Test sprawdzający metodę get_meals"""
    plan = MealPlan()
    recipe1 = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)
    recipe2 = Recipe("Pancake", {"flour": 100}, 200, 6, 8, 30)

    plan.add_meal("Monday", recipe1)
    plan.add_meal("Monday", recipe2)

    meals = plan.get_meals("Monday")
    assert len(meals) == 2
    assert meals[0].name == "Toast"


def test_clear_day():
    """Test sprawdzający metodę clear_day"""
    plan = MealPlan()
    recipe1 = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)
    recipe2 = Recipe("Pancake", {"flour": 100}, 200, 6, 8, 30)

    plan.add_meal("Monday", recipe1)
    plan.add_meal("Monday", recipe2)
    plan.clear_day("Monday")

    assert len(plan.plan["Monday"]) == 0


#############################################
# Testy wydajnościowe i skrajnych przypadków #
#############################################

def test_mealplan_with_100_recipes():
    """Test sprawdza wydajność przy dodaniu 100 przepisów w jednym dniu."""
    plan = MealPlan()
    recipe = Recipe("Mass", {"ingredient": 1}, 100, 1, 1, 1)

    for _ in range(100):
        plan.add_meal("Sunday", recipe)

    assert len(plan.get_meals("Sunday")) == 100
    assert plan.daily_summary("Sunday")["kcal"] == 100 * 100


def test_mealplan_performance_with_many_recipes(benchmark):
    """Test wydajnościowy dodawania wielu przepisów"""
    recipe = Recipe("Performance", {"ing": 1}, 100, 1, 1, 1)

    def add_many():
        plan = MealPlan()
        for _ in range(1000):
            plan.add_meal("Monday", recipe)
        return plan

    result = benchmark(add_many)
    assert len(result.get_meals("Monday")) == 1000


def test_full_week_plan():
    """Test sprawdzający utworzenie pełnego tygodniowego planu posiłków"""
    mp = MealPlan()
    breakfast = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
    lunch = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)
    dinner = Recipe("Dinner", {"chicken": 200}, 300, 30, 10, 0)

    for day in mp.plan.keys():
        mp.add_meal(day, breakfast)
        mp.add_meal(day, lunch)
        mp.add_meal(day, dinner)
        assert len(mp.plan[day]) == 3

    summary = mp.daily_summary("Sunday")
    assert summary["kcal"] == 630