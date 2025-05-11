import pytest
from shoppinglist import generate_shopping_list, ShoppingList
from mealplan import MealPlan
from recipe import Recipe


# Fixture definiujący prosty przepis
@pytest.fixture
def basic_recipe():
    return Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)


# Fixture definiujący bardziej złożony przepis
@pytest.fixture
def complex_recipe():
    return Recipe("Sandwich", {"bread": 2, "cheese": 1, "tomato": 1}, 250, 10, 8, 30)


# Fixture tworzący zestaw przykładowych przepisów
@pytest.fixture
def sample_recipes():
    return [
        Recipe(
            "Pasta", {"pasta": 100, "tomato_sauce": 50, "cheese": 20}, 450, 15, 10, 60
        ),
        Recipe("Salad", {"lettuce": 100, "tomato": 2, "cucumber": 1}, 120, 3, 2, 15),
        Recipe("Omelette", {"eggs": 3, "cheese": 30, "pepper": 1}, 320, 22, 18, 4),
        Recipe("Smoothie", {"banana": 1, "milk": 200, "strawberry": 50}, 180, 5, 3, 30),
    ]


# Fixture tworzący plan posiłków z przepisami
@pytest.fixture
def meal_plan_with_recipes(sample_recipes):
    plan = MealPlan()
    plan.add_meal("Monday", sample_recipes[0])  # Pasta
    plan.add_meal("Monday", sample_recipes[1])  # Salad
    plan.add_meal("Tuesday", sample_recipes[2])  # Omelette
    plan.add_meal("Wednesday", sample_recipes[0])  # Pasta again
    plan.add_meal("Friday", sample_recipes[3])  # Smoothie
    return plan


# Test funkcji generate_shopping_list z różnymi zestawami przepisów i oczekiwanymi wynikami
@pytest.mark.parametrize(
    "recipes,expected",
    [
        (
            [
                Recipe("Test1", {"milk": 200}, 100, 5, 3, 10),
                Recipe("Test2", {"milk": 100, "bread": 2}, 150, 6, 4, 20),
            ],
            {"milk": 300, "bread": 2},
        ),
        (
            [
                Recipe("Test3", {"apple": 1}, 50, 1, 0, 12),
            ],
            {"apple": 1},
        ),
        (
            [
                Recipe("Test4", {"rice": 100}, 200, 4, 2, 45),
                Recipe("Test5", {"rice": 150, "chicken": 200}, 400, 30, 10, 0),
            ],
            {"rice": 250, "chicken": 200},
        ),
        (
            [
                Recipe("Combo", {"tomato": 100, "cheese": 50}, 200, 10, 8, 12),
                Recipe("Salad", {"tomato": 50, "lettuce": 100}, 100, 2, 1, 5),
            ],
            {"tomato": 150, "cheese": 50, "lettuce": 100},
        ),
        (
            [
                Recipe("Breakfast", {"eggs": 2, "bread": 100}, 250, 15, 5, 30),
                Recipe("Lunch", {"rice": 150, "chicken": 200}, 400, 35, 10, 50),
                Recipe("Dinner", {"chicken": 150, "vegetables": 300}, 350, 30, 8, 20),
            ],
            {"eggs": 2, "bread": 100, "rice": 150, "chicken": 350, "vegetables": 300},
        ),
    ],
)
def test_generate_shopping_list(recipes, expected):
    shopping_list = generate_shopping_list(recipes)
    assert shopping_list == expected


# Test sprawdzający czy funkcja zwraca pusty słownik dla pustej listy przepisów
def test_generate_shopping_list_empty():
    shopping_list = generate_shopping_list([])
    assert shopping_list == {}


# Test sprawdzający czy funkcja poprawnie obsługuje duplikaty przepisów
def test_generate_shopping_list_duplicate_recipes(basic_recipe):
    shopping_list = generate_shopping_list([basic_recipe, basic_recipe, basic_recipe])
    assert shopping_list == {"bread": 6}  # 3 x 2 pieczywa


# Test sprawdzający poprawność inicjalizacji obiektu ShoppingList
def test_shopping_list_init():
    sl = ShoppingList()
    assert len(sl.items) == 0


# Test sprawdzający dodawanie produktów do listy zakupów
def test_add_item():
    sl = ShoppingList()
    sl.add_item("apple", 5)
    assert len(sl.items) == 1
    assert sl.items["apple"] == 5

    # Test adding same item multiple times
    sl.add_item("apple", 3)
    assert sl.items["apple"] == 8


# Test sprawdzający czy funkcja ignoruje dodawanie produktów z ujemną ilością
def test_add_item_negative_quantity():
    sl = ShoppingList()
    sl.add_item("apple", -3)  # Powinno ignorować ujemne ilości
    assert "apple" not in sl.items


# Test sprawdzający czy funkcja ignoruje dodawanie produktów z zerową ilością
def test_add_item_zero_quantity():
    sl = ShoppingList()
    sl.add_item("apple", 0)
    assert "apple" not in sl.items


# Test sprawdzający poprawność zwracania wszystkich produktów z listy
def test_get_items():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)

    items = sl.get_items()
    assert isinstance(items, dict)
    assert items["flour"] == 500
    assert items["sugar"] == 250


# Test sprawdzający dodawanie produktów z przepisu do listy zakupów
def test_add_from_recipe(basic_recipe):
    # Test z pojedynczym przepisem
    sl = ShoppingList()
    sl.add_from_recipe(basic_recipe)
    items = sl.get_items()
    assert len(items) == 1
    assert items["bread"] == 2

    # Test z bardziej złożonym przepisem
    sl = ShoppingList()
    recipe = Recipe("Pancakes", {"flour": 200, "milk": 300, "eggs": 2}, 450, 15, 10, 60)
    sl.add_from_recipe(recipe)
    assert sl.items["flour"] == 200
    assert sl.items["milk"] == 300
    assert sl.items["eggs"] == 2


# Test sprawdzający dodawanie produktów z przepisów do listy z istniejącymi produktami
def test_add_from_recipe_with_existing_items(basic_recipe, complex_recipe):
    # Test dodawania wielu przepisów
    sl = ShoppingList()
    sl.add_from_recipe(basic_recipe)
    sl.add_from_recipe(complex_recipe)
    items = sl.get_items()
    assert len(items) == 3
    assert items["bread"] == 4  # 2 + 2
    assert items["cheese"] == 1
    assert items["tomato"] == 1

    # Test dodawania z istniejącymi składnikami
    sl = ShoppingList()
    sl.add_item("flour", 100)
    sl.add_item("sugar", 50)

    recipe = Recipe("Cookies", {"flour": 200, "butter": 100}, 400, 5, 20, 40)
    sl.add_from_recipe(recipe)

    assert sl.items["flour"] == 300
    assert sl.items["sugar"] == 50
    assert sl.items["butter"] == 100


# Test sprawdzający dodawanie produktów z planu posiłków do listy zakupów
def test_add_from_mealplan():
    sl = ShoppingList()
    mp = MealPlan()

    recipe1 = Recipe("Breakfast", {"eggs": 2, "bread": 100}, 250, 15, 5, 30)
    recipe2 = Recipe("Lunch", {"rice": 150, "chicken": 200}, 400, 35, 10, 50)

    mp.add_meal("Monday", recipe1)
    mp.add_meal("Tuesday", recipe2)

    sl.add_from_mealplan(mp)

    assert sl.items["eggs"] == 2
    assert sl.items["bread"] == 100
    assert sl.items["rice"] == 150
    assert sl.items["chicken"] == 200


# Test sprawdzający filtrowanie produktów według minimalnej ilości
def test_filter_by_threshold():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 50)
    sl.add_item("butter", 200)
    sl.add_item("salt", 5)

    filtered = sl.filter_by_threshold(100)
    filtered_items = filtered.get_items()

    assert "flour" in filtered_items
    assert "butter" in filtered_items
    assert "sugar" not in filtered_items
    assert "salt" not in filtered_items


# Test sprawdzający usuwanie produktów z listy zakupów
def test_remove_item():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    sl.add_item("orange", 10)

    sl.remove_item("sugar")
    assert "flour" in sl.items
    assert "sugar" not in sl.items
    assert "orange" in sl.items

    # Test removing nonexistent item
    sl.remove_item("nonexistent")
    assert len(sl.items) == 2
    assert sl.items["flour"] == 500


# Test sprawdzający czyszczenie całej listy zakupów
def test_clear():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    sl.add_item("butter", 200)

    sl.clear()
    assert len(sl.items) == 0


# Test sprawdzający aktualizację ilości produktu na liście
def test_update_item_quantity():
    sl = ShoppingList()
    sl.add_item("flour", 500)

    sl.update_item_quantity("flour", 750)
    assert sl.items["flour"] == 750

    # Test update with negative value
    sl.update_item_quantity("flour", -100)
    assert sl.items["flour"] == 750

    # Test update nonexistent item
    sl.update_item_quantity("sugar", 250)
    assert "sugar" not in sl.items


# Test sprawdzający zliczanie ilości różnych produktów na liście
def test_get_total_items():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    sl.add_item("butter", 200)

    assert sl.get_total_items() == 3


# Test sprawdzający obliczanie sumy wszystkich ilości produktów
def test_get_total_quantity():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    sl.add_item("butter", 200)

    assert sl.get_total_quantity() == 950


# Test sprawdzający kategoryzację produktów na liście
def test_get_categorized_items():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)

    categories = sl.get_categorized_items()

    assert "uncategorized" in categories
    assert "flour" in categories["uncategorized"]
    assert "sugar" in categories["uncategorized"]


# Test sprawdzający czy produkt znajduje się na liście
def test_has_item():
    sl = ShoppingList()
    sl.add_item("flour", 500)

    assert sl.has_item("flour") is True
    assert sl.has_item("sugar") is False


# Test sprawdzający pobieranie ilości produktu z listy
def test_get_item_quantity():
    sl = ShoppingList()
    sl.add_item("flour", 500)

    assert sl.get_item_quantity("flour") == 500
    assert sl.get_item_quantity("nonexistent") == 0


# Test sprawdzający eksport listy zakupów do słownika
def test_export():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)

    exported = sl.export()

    assert isinstance(exported, dict)
    assert exported["flour"] == 500
    assert exported["sugar"] == 250


# Test sprawdzający import listy zakupów ze słownika
def test_import_list():
    sl = ShoppingList()
    data = {"flour": 500, "sugar": 250}

    sl.import_list(data)

    assert sl.items["flour"] == 500
    assert sl.items["sugar"] == 250


# Test sprawdzający łączenie dwóch list zakupów
def test_merge():
    sl1 = ShoppingList()
    sl1.add_item("flour", 500)
    sl1.add_item("sugar", 250)

    sl2 = ShoppingList()
    sl2.add_item("butter", 200)
    sl2.add_item("flour", 300)

    merged = sl1.merge(sl2)

    assert merged.items["flour"] == 800
    assert merged.items["sugar"] == 250
    assert merged.items["butter"] == 200


# Test sprawdzający skalowanie ilości produktów na liście
def test_scale_quantities():
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)

    sl.scale_quantities(2)

    assert sl.items["flour"] == 1000
    assert sl.items["sugar"] == 500

    # Test zero factor
    sl.scale_quantities(0)
    assert sl.items["flour"] == 0
    assert sl.items["sugar"] == 0


# Test sprawdzający obsługę błędu przy próbie skalowania ujemnym współczynnikiem
def test_scale_quantities_negative_factor():
    sl = ShoppingList()
    sl.add_item("flour", 500)

    with pytest.raises(ValueError, match="Scale factor must be non-negative"):
        sl.scale_quantities(-1)

    assert sl.items["flour"] == 500
