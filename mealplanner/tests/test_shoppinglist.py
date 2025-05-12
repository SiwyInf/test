import pytest
from unittest.mock import Mock
from src.shoppinglist import generate_shopping_list, ShoppingList
from src.mealplan import MealPlan
from src.recipe import Recipe

#############################################
# Fixtures #
#############################################

@pytest.fixture
def basic_recipe():
    return Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)

@pytest.fixture
def complex_recipe():
    return Recipe("Sandwich", {"bread": 2, "cheese": 1, "tomato": 1}, 250, 10, 8, 30)

@pytest.fixture
def sample_recipes():
    return [
        Recipe("Pasta", {"pasta": 100, "tomato_sauce": 50, "cheese": 20}, 450, 15, 10, 60),
        Recipe("Salad", {"lettuce": 100, "tomato": 2, "cucumber": 1}, 120, 3, 2, 15),
        Recipe("Omelette", {"eggs": 3, "cheese": 30, "pepper": 1}, 320, 22, 18, 4),
        Recipe("Smoothie", {"banana": 1, "milk": 200, "strawberry": 50}, 180, 5, 3, 30),
    ]

@pytest.fixture
def meal_plan_with_recipes(sample_recipes):
    plan = MealPlan()
    plan.add_meal("Monday", sample_recipes[0])
    plan.add_meal("Monday", sample_recipes[1])
    plan.add_meal("Tuesday", sample_recipes[2])
    plan.add_meal("Wednesday", sample_recipes[0])
    plan.add_meal("Friday", sample_recipes[3])
    return plan

#############################################
# Testy dla funkcji generate_shopping_list #
#############################################

@pytest.mark.parametrize("recipes,expected", [
    ([Recipe("Test1", {"milk": 200}, 100, 5, 3, 10), Recipe("Test2", {"milk": 100, "bread": 2}, 150, 6, 4, 20)], {"milk": 300, "bread": 2}),
    ([Recipe("Test3", {"apple": 1}, 50, 1, 0, 12)], {"apple": 1}),
    ([Recipe("Test4", {"rice": 100}, 200, 4, 2, 45), Recipe("Test5", {"rice": 150, "chicken": 200}, 400, 30, 10, 0)], {"rice": 250, "chicken": 200}),
    ([Recipe("Combo", {"tomato": 100, "cheese": 50}, 200, 10, 8, 12), Recipe("Salad", {"tomato": 50, "lettuce": 100}, 100, 2, 1, 5)], {"tomato": 150, "cheese": 50, "lettuce": 100}),
    ([Recipe("Breakfast", {"eggs": 2, "bread": 100}, 250, 15, 5, 30), Recipe("Lunch", {"rice": 150, "chicken": 200}, 400, 35, 10, 50), Recipe("Dinner", {"chicken": 150, "vegetables": 300}, 350, 30, 8, 20)], {"eggs": 2, "bread": 100, "rice": 150, "chicken": 350, "vegetables": 300}),
])
def test_generate_shopping_list(recipes, expected):
    """Test generating shopping list from various recipe combinations"""
    assert generate_shopping_list(recipes) == expected

def test_generate_shopping_list_empty():
    """Test empty recipe list handling"""
    assert generate_shopping_list([]) == {}

def test_generate_shopping_list_duplicate_recipes(basic_recipe):
    """Test handling duplicate recipes"""
    assert generate_shopping_list([basic_recipe, basic_recipe, basic_recipe]) == {"bread": 6}

#############################################
# Testy podstawowych operacji ShoppingList #
#############################################

def test_shopping_list_init():
    """Test shopping list initialization"""
    sl = ShoppingList()
    assert len(sl.items) == 0

def test_add_item():
    """Test adding items to shopping list"""
    sl = ShoppingList()
    sl.add_item("apple", 5)
    assert sl.items["apple"] == 5
    sl.add_item("apple", 3)
    assert sl.items["apple"] == 8

@pytest.mark.parametrize("quantity,should_exist", [(-3, False), (0, False), (1, True)])
def test_add_item_edge_cases(quantity, should_exist):
    """Test edge cases for adding items"""
    sl = ShoppingList()
    sl.add_item("apple", quantity)
    assert ("apple" in sl.items) == should_exist

def test_get_items():
    """Test retrieving all items"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    items = sl.get_items()
    assert items == {"flour": 500, "sugar": 250}

def test_remove_item():
    """Test removing items from shopping list"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    sl.remove_item("sugar")
    assert "sugar" not in sl.items
    assert "flour" in sl.items

def test_clear():
    """Test clearing shopping list"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.clear()
    assert len(sl.items) == 0

def test_update_item_quantity():
    """Test updating item quantities"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.update_item_quantity("flour", 750)
    assert sl.items["flour"] == 750
    sl.update_item_quantity("flour", -100)
    assert sl.items["flour"] == 750  # Should not update with negative

#############################################
# Testy integracji przepisów ShoppingList #
#############################################

def test_add_from_recipe(basic_recipe):
    """Test adding ingredients from recipe"""
    sl = ShoppingList()
    sl.add_from_recipe(basic_recipe)
    assert sl.items["bread"] == 2

def test_add_from_recipe_with_existing_items(basic_recipe, complex_recipe):
    """Test adding multiple recipes with overlapping ingredients"""
    sl = ShoppingList()
    sl.add_from_recipe(basic_recipe)
    sl.add_from_recipe(complex_recipe)
    assert sl.items["bread"] == 4
    assert sl.items["cheese"] == 1

def test_add_from_mealplan(meal_plan_with_recipes):
    """Test adding recipes from meal plan"""
    sl = ShoppingList()
    sl.add_from_mealplan(meal_plan_with_recipes)
    assert sl.items["pasta"] == 200  # Added twice
    assert sl.items["eggs"] == 3

def test_shoppinglist_with_duplicate_ingredients():
    """Test sprawdza, czy lista zakupów łączy składniki o tej samej nazwie."""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("flour", 300)
    assert sl.get_items() == {"flour": 800}

def test_shoppinglist_with_empty_recipe():
    """Test ShoppingList z przepisem bez składników"""
    sl = ShoppingList()
    empty_recipe = Recipe("Empty", {}, 0, 0, 0, 0)
    sl.add_from_recipe(empty_recipe)
    assert sl.get_items() == {}

#############################################
# Testy zaawansowanych operacji ShoppingList #
#############################################

def test_filter_by_threshold():
    """Test filtering items by quantity threshold"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 50)
    filtered = sl.filter_by_threshold(100).get_items()
    assert "flour" in filtered
    assert "sugar" not in filtered

def test_get_total_items():
    """Test counting unique items"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    assert sl.get_total_items() == 2

def test_get_total_quantity():
    """Test calculating total quantity"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.add_item("sugar", 250)
    assert sl.get_total_quantity() == 750

def test_get_categorized_items():
    """Test item categorization"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    categories = sl.get_categorized_items()
    assert "flour" in categories["uncategorized"]

def test_has_item():
    """Test checking item existence"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    assert sl.has_item("flour")
    assert not sl.has_item("sugar")

def test_get_item_quantity():
    """Test getting item quantity"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    assert sl.get_item_quantity("flour") == 500
    assert sl.get_item_quantity("sugar") == 0

#############################################
# Testy importu/eksportu ShoppingList #
#############################################

def test_export():
    """Test exporting shopping list"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    exported = sl.export()
    assert exported == {"flour": 500}

def test_import_list():
    """Test importing shopping list"""
    sl = ShoppingList()
    sl.import_list({"flour": 500})
    assert sl.items["flour"] == 500

def test_merge():
    """Test merging shopping lists"""
    sl1 = ShoppingList()
    sl1.add_item("flour", 500)
    sl2 = ShoppingList()
    sl2.add_item("flour", 300)
    merged = sl1.merge(sl2)
    assert merged.items["flour"] == 800

def test_shoppinglist_export_import_consistency():
    """Test sprawdzający spójność eksportu i importu"""
    sl1 = ShoppingList()
    sl1.add_item("a", 1)
    sl1.add_item("b", 2)
    exported = sl1.export()
    sl2 = ShoppingList()
    sl2.import_list(exported)
    assert sl1.get_items() == sl2.get_items()

#############################################
# Testy skalowania listy zakupów #
#############################################

def test_scale_quantities():
    """Test scaling quantities"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    sl.scale_quantities(2)
    assert sl.items["flour"] == 1000
    sl.scale_quantities(0)
    assert sl.items["flour"] == 0

def test_scale_quantities_negative_factor():
    """Test handling negative scale factors"""
    sl = ShoppingList()
    sl.add_item("flour", 500)
    with pytest.raises(ValueError):
        sl.scale_quantities(-1)
    assert sl.items["flour"] == 500

#############################################
# Testy dla ShoppingList z mocks #
#############################################

def test_shopping_list_with_mocked_recipe():
    """Test sprawdzający ShoppingList z mockowanym Recipe"""
    mock_ingredients = Mock()
    mock_ingredients.items.return_value = [("mock_ingredient", 100)]
    mock_recipe = Mock()
    mock_recipe.ingredients = mock_ingredients
    sl = ShoppingList()
    sl.add_from_recipe(mock_recipe)
    assert sl.get_items() == {"mock_ingredient": 100}
    mock_ingredients.items.assert_called_once()

#############################################
# Testy integracyjne #
#############################################

def test_integration_mealplan_shoppinglist():
    """Test integracyjny MealPlan i ShoppingList"""
    plan = MealPlan()
    recipe1 = Recipe("R1", {"a": 1, "b": 2}, 100, 1, 1, 1)
    recipe2 = Recipe("R2", {"a": 3, "c": 4}, 200, 2, 2, 2)
    plan.add_meal("Monday", recipe1)
    plan.add_meal("Tuesday", recipe2)
    sl = ShoppingList()
    sl.add_from_mealplan(plan)
    assert sl.get_items() == {"a": 4, "b": 2, "c": 4}