import pytest
from mealplan import MealPlan
from recipe import Recipe


# Fixture definiujący podstawowy przepis, który będzie używany w wielu testach
@pytest.fixture
def basic_recipe():
    return Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)


# Test sprawdzający dodawanie posiłków do planu dla każdego dnia tygodnia i poprawność podsumowania dziennego
@pytest.mark.parametrize(
    "day",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
)
def test_add_meal_and_summary(basic_recipe, day):
    plan = MealPlan()
    plan.add_meal(day, basic_recipe)
    summary = plan.daily_summary(day)
    assert summary["kcal"] == 150
    assert summary["protein"] == 5
    assert summary["fat"] == 2
    assert summary["carbs"] == 20


# Test sprawdzający, czy dodanie posiłku do nieprawidłowego dnia wywołuje błąd ValueError
@pytest.mark.parametrize("invalid_day", ["Funday", "Yesterday", "", None])
def test_invalid_day_meal_add_raises(basic_recipe, invalid_day):
    plan = MealPlan()
    with pytest.raises(ValueError):
        plan.add_meal(invalid_day, basic_recipe)


# Test sprawdzający poprawność sumowania wartości odżywczych dla wielu różnych przepisów w jednym dniu
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
        ("Thursday", [Recipe("F", {"c": 1}, 300, 25, 12, 15)]),
        ("Friday", [Recipe("G", {"d": 2}, 180, 12, 9, 8)]),
        ("Saturday", [Recipe("H", {"e": 1}, 90, 5, 2, 6)]),
        ("Sunday", [Recipe("I", {"f": 3}, 250, 20, 15, 10)]),
    ],
)
def test_multiple_recipes_daily_summary(day, recipes):
    plan = MealPlan()
    for r in recipes:
        plan.add_meal(day, r)
    total_kcal = sum(r.kcal for r in recipes)
    total_protein = sum(r.protein for r in recipes)
    total_fat = sum(r.fat for r in recipes)
    total_carbs = sum(r.carbs for r in recipes)
    summary = plan.daily_summary(day)
    assert summary["kcal"] == total_kcal
    assert summary["protein"] == total_protein
    assert summary["fat"] == total_fat
    assert summary["carbs"] == total_carbs


# Test sprawdzający podsumowanie dla dni bez żadnych posiłków
@pytest.mark.parametrize("day", ["Monday", "Tuesday", "Wednesday"])
def test_mealplan_with_empty_day(day):
    plan = MealPlan()
    plan.plan[day] = []  # Jawnie pusto
    assert plan.daily_summary(day) == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}


# Test sprawdzający wielokrotne dodawanie tego samego przepisu i sumowanie wartości odżywczych
def test_mealplan_adding_same_recipe_multiple_times():
    plan = MealPlan()
    r = Recipe("Repeat", {"x": 1}, 100, 5, 5, 5)
    for _ in range(10):
        plan.add_meal("Friday", r)
    summary = plan.daily_summary("Friday")
    assert summary["kcal"] == 1000
    assert summary["protein"] == 50
    assert summary["fat"] == 50
    assert summary["carbs"] == 50


# Test sprawdzający dodawanie tego samego posiłku do różnych dni
@pytest.mark.parametrize(
    "day",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
)
def test_mealplan_adding_same_meal_to_different_days(day):
    plan = MealPlan()
    r = Recipe("Multi", {"a": 1}, 100, 10, 1, 1)
    plan.add_meal(day, r)
    assert plan.daily_summary(day)["kcal"] == 100


# Test sprawdzający sumowanie wartości odżywczych dla dużej liczby (100) posiłków
def test_mealplan_100_meals_summary_correct():
    plan = MealPlan()
    r = Recipe("R", {"z": 1}, 10, 1, 1, 1)
    for _ in range(100):
        plan.add_meal("Monday", r)
    assert plan.daily_summary("Monday")["kcal"] == 1000
    assert plan.daily_summary("Monday")["protein"] == 100
    assert plan.daily_summary("Monday")["fat"] == 100
    assert plan.daily_summary("Monday")["carbs"] == 100


# Test sprawdzający poprawność podsumowania dla różnych przepisów w jednym dniu
def test_mealplan_summary_multiple_recipes_varied():
    plan = MealPlan()
    r1 = Recipe("L1", {"a": 1}, 50, 2, 1, 5)
    r2 = Recipe("L2", {"b": 1}, 100, 3, 1, 10)
    plan.add_meal("Wednesday", r1)
    plan.add_meal("Wednesday", r2)
    summary = plan.daily_summary("Wednesday")
    assert summary["kcal"] == 150
    assert summary["protein"] == 5
    assert summary["fat"] == 2
    assert summary["carbs"] == 15


# Test sprawdzający reakcję na próbę dodania nieprawidłowego typu przepisu
def test_mealplan_invalid_recipe_type():
    plan = MealPlan()
    with pytest.raises(TypeError):
        plan.add_meal("Monday", "not_a_recipe")  # Niepoprawny typ


# Test sprawdzający poprawność inicjalizacji pustego planu posiłków
def test_mealplan_initialization():
    plan = MealPlan()
    # Sprawdź czy wszystkie dni są inicjalizowane
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


# Test sprawdzający dodawanie wielu posiłków do tego samego dnia
def test_add_multiple_meals_to_same_day():
    mp = MealPlan()
    recipe1 = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
    recipe2 = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)
    recipe3 = Recipe("Dinner", {"chicken": 200}, 300, 30, 10, 0)

    mp.add_meal("Wednesday", recipe1)
    mp.add_meal("Wednesday", recipe2)
    mp.add_meal("Wednesday", recipe3)

    assert len(mp.plan["Wednesday"]) == 3
    assert mp.plan["Wednesday"][0].name == "Breakfast"
    assert mp.plan["Wednesday"][2].name == "Dinner"

    summary = mp.daily_summary("Wednesday")
    assert summary["kcal"] == 630  # 180 + 150 + 300
    assert summary["protein"] == 45  # 12 + 3 + 30
    assert summary["fat"] == 21  # 10 + 1 + 10
    assert summary["carbs"] == 35  # 5 + 30 + 0


# Test sprawdzający reakcję na próbę pobrania podsumowania dla nieistniejącego dnia
def test_mealplan_invalid_day_summary():
    plan = MealPlan()
    with pytest.raises(ValueError):
        plan.daily_summary("NonExistentDay")


# Test sprawdzający wielokrotne dodawanie tego samego obiektu przepisu
def test_add_same_recipe_multiple_times():
    mp = MealPlan()
    recipe = Recipe("Snack", {"nuts": 50}, 280, 10, 22, 8)

    mp.add_meal("Monday", recipe)
    mp.add_meal("Monday", recipe)  # Same instance added twice

    assert len(mp.plan["Monday"]) == 2
    summary = mp.daily_summary("Monday")
    assert summary["kcal"] == 560  # 280 + 280


# Test sprawdzający utworzenie pełnego tygodniowego planu posiłków
def test_full_week_plan():
    mp = MealPlan()
    breakfast = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
    lunch = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)
    dinner = Recipe("Dinner", {"chicken": 200}, 300, 30, 10, 0)

    # Dodawanie posilkow na kazdy dzien
    for day in mp.plan.keys():
        mp.add_meal(day, breakfast)
        mp.add_meal(day, lunch)
        mp.add_meal(day, dinner)

    # Sprawdzanie wszyzstkich dni
    for day in mp.plan.keys():
        assert len(mp.plan[day]) == 3

    # sprawdzanie wartosci odzywczych wszystkich dni
    summary = mp.daily_summary("Sunday")
    assert summary["kcal"] == 630  # 180 + 150 + 300
    assert summary["protein"] == 45  # 12 + 3 + 30
    assert summary["fat"] == 21  # 10 + 1 + 10
    assert summary["carbs"] == 35  # 5 + 30 + 0
