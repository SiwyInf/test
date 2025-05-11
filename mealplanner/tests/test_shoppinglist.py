import unittest
from src.shoppinglist import generate_shopping_list, ShoppingList
from src.mealplan import MealPlan
from src.recipe import Recipe


class TestShoppingList(unittest.TestCase):
    def setUp(self):
        # Basic recipe fixture
        self.basic_recipe = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)

        # Complex recipe fixture
        self.complex_recipe = Recipe("Sandwich", {"bread": 2, "cheese": 1, "tomato": 1}, 250, 10, 8, 30)

        # Sample recipes fixture
        self.sample_recipes = [
            Recipe("Pasta", {"pasta": 100, "tomato_sauce": 50, "cheese": 20}, 450, 15, 10, 60),
            Recipe("Salad", {"lettuce": 100, "tomato": 2, "cucumber": 1}, 120, 3, 2, 15),
            Recipe("Omelette", {"eggs": 3, "cheese": 30, "pepper": 1}, 320, 22, 18, 4),
            Recipe("Smoothie", {"banana": 1, "milk": 200, "strawberry": 50}, 180, 5, 3, 30),
        ]

        # Meal plan with recipes fixture
        self.meal_plan_with_recipes = MealPlan()
        self.meal_plan_with_recipes.add_meal("Monday", self.sample_recipes[0])  # Pasta
        self.meal_plan_with_recipes.add_meal("Monday", self.sample_recipes[1])  # Salad
        self.meal_plan_with_recipes.add_meal("Tuesday", self.sample_recipes[2])  # Omelette
        self.meal_plan_with_recipes.add_meal("Wednesday", self.sample_recipes[0])  # Pasta again
        self.meal_plan_with_recipes.add_meal("Friday", self.sample_recipes[3])  # Smoothie

    def test_generate_shopping_list_param1(self):
        recipes = [
            Recipe("Test1", {"milk": 200}, 100, 5, 3, 10),
            Recipe("Test2", {"milk": 100, "bread": 2}, 150, 6, 4, 20),
        ]
        expected = {"milk": 300, "bread": 2}
        shopping_list = generate_shopping_list(recipes)
        self.assertEqual(shopping_list, expected)

    def test_generate_shopping_list_param2(self):
        recipes = [
            Recipe("Test3", {"apple": 1}, 50, 1, 0, 12),
        ]
        expected = {"apple": 1}
        shopping_list = generate_shopping_list(recipes)
        self.assertEqual(shopping_list, expected)

    def test_generate_shopping_list_param3(self):
        recipes = [
            Recipe("Test4", {"rice": 100}, 200, 4, 2, 45),
            Recipe("Test5", {"rice": 150, "chicken": 200}, 400, 30, 10, 0),
        ]
        expected = {"rice": 250, "chicken": 200}
        shopping_list = generate_shopping_list(recipes)
        self.assertEqual(shopping_list, expected)

    def test_generate_shopping_list_param4(self):
        recipes = [
            Recipe("Combo", {"tomato": 100, "cheese": 50}, 200, 10, 8, 12),
            Recipe("Salad", {"tomato": 50, "lettuce": 100}, 100, 2, 1, 5),
        ]
        expected = {"tomato": 150, "cheese": 50, "lettuce": 100}
        shopping_list = generate_shopping_list(recipes)
        self.assertEqual(shopping_list, expected)

    def test_generate_shopping_list_param5(self):
        recipes = [
            Recipe("Breakfast", {"eggs": 2, "bread": 100}, 250, 15, 5, 30),
            Recipe("Lunch", {"rice": 150, "chicken": 200}, 400, 35, 10, 50),
            Recipe("Dinner", {"chicken": 150, "vegetables": 300}, 350, 30, 8, 20),
        ]
        expected = {"eggs": 2, "bread": 100, "rice": 150, "chicken": 350, "vegetables": 300}
        shopping_list = generate_shopping_list(recipes)
        self.assertEqual(shopping_list, expected)

    def test_generate_shopping_list_empty(self):
        shopping_list = generate_shopping_list([])
        self.assertEqual(shopping_list, {})

    def test_generate_shopping_list_duplicate_recipes(self):
        shopping_list = generate_shopping_list([self.basic_recipe, self.basic_recipe, self.basic_recipe])
        self.assertEqual(shopping_list, {"bread": 6})  # 3 x 2 pieczywa

    def test_shopping_list_init(self):
        sl = ShoppingList()
        self.assertEqual(len(sl.items), 0)

    def test_add_item(self):
        sl = ShoppingList()
        sl.add_item("apple", 5)
        self.assertEqual(len(sl.items), 1)
        self.assertEqual(sl.items["apple"], 5)

        # Test adding same item multiple times
        sl.add_item("apple", 3)
        self.assertEqual(sl.items["apple"], 8)

    def test_add_item_negative_quantity(self):
        sl = ShoppingList()
        sl.add_item("apple", -3)  # Powinno ignorować ujemne ilości
        self.assertNotIn("apple", sl.items)

    def test_add_item_zero_quantity(self):
        sl = ShoppingList()
        sl.add_item("apple", 0)
        self.assertNotIn("apple", sl.items)

    def test_get_items(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)

        items = sl.get_items()
        self.assertIsInstance(items, dict)
        self.assertEqual(items["flour"], 500)
        self.assertEqual(items["sugar"], 250)

    def test_add_from_recipe_simple(self):
        # Test z pojedynczym przepisem
        sl = ShoppingList()
        sl.add_from_recipe(self.basic_recipe)
        items = sl.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items["bread"], 2)

    def test_add_from_recipe_complex(self):
        # Test z bardziej złożonym przepisem
        sl = ShoppingList()
        recipe = Recipe("Pancakes", {"flour": 200, "milk": 300, "eggs": 2}, 450, 15, 10, 60)
        sl.add_from_recipe(recipe)
        self.assertEqual(sl.items["flour"], 200)
        self.assertEqual(sl.items["milk"], 300)
        self.assertEqual(sl.items["eggs"], 2)

    def test_add_from_recipe_with_existing_items(self):
        # Test dodawania wielu przepisów
        sl = ShoppingList()
        sl.add_from_recipe(self.basic_recipe)
        sl.add_from_recipe(self.complex_recipe)
        items = sl.get_items()
        self.assertEqual(len(items), 3)
        self.assertEqual(items["bread"], 4)  # 2 + 2
        self.assertEqual(items["cheese"], 1)
        self.assertEqual(items["tomato"], 1)

    def test_add_from_recipe_with_preexisting_ingredients(self):
        # Test dodawania z istniejącymi składnikami
        sl = ShoppingList()
        sl.add_item("flour", 100)
        sl.add_item("sugar", 50)

        recipe = Recipe("Cookies", {"flour": 200, "butter": 100}, 400, 5, 20, 40)
        sl.add_from_recipe(recipe)

        self.assertEqual(sl.items["flour"], 300)
        self.assertEqual(sl.items["sugar"], 50)
        self.assertEqual(sl.items["butter"], 100)

    def test_add_from_mealplan(self):
        sl = ShoppingList()
        mp = MealPlan()

        recipe1 = Recipe("Breakfast", {"eggs": 2, "bread": 100}, 250, 15, 5, 30)
        recipe2 = Recipe("Lunch", {"rice": 150, "chicken": 200}, 400, 35, 10, 50)

        mp.add_meal("Monday", recipe1)
        mp.add_meal("Tuesday", recipe2)

        sl.add_from_mealplan(mp)

        self.assertEqual(sl.items["eggs"], 2)
        self.assertEqual(sl.items["bread"], 100)
        self.assertEqual(sl.items["rice"], 150)
        self.assertEqual(sl.items["chicken"], 200)

    def test_filter_by_threshold(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 50)
        sl.add_item("butter", 200)
        sl.add_item("salt", 5)

        filtered = sl.filter_by_threshold(100)
        filtered_items = filtered.get_items()

        self.assertIn("flour", filtered_items)
        self.assertIn("butter", filtered_items)
        self.assertNotIn("sugar", filtered_items)
        self.assertNotIn("salt", filtered_items)

    def test_remove_item(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)
        sl.add_item("orange", 10)

        sl.remove_item("sugar")
        self.assertIn("flour", sl.items)
        self.assertNotIn("sugar", sl.items)
        self.assertIn("orange", sl.items)

        # Test removing nonexistent item
        sl.remove_item("nonexistent")
        self.assertEqual(len(sl.items), 2)
        self.assertEqual(sl.items["flour"], 500)

    def test_clear(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)
        sl.add_item("butter", 200)

        sl.clear()
        self.assertEqual(len(sl.items), 0)

    def test_update_item_quantity(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)

        sl.update_item_quantity("flour", 750)
        self.assertEqual(sl.items["flour"], 750)

        # Test update with negative value
        sl.update_item_quantity("flour", -100)
        self.assertEqual(sl.items["flour"], 750)

        # Test update nonexistent item
        sl.update_item_quantity("sugar", 250)
        self.assertNotIn("sugar", sl.items)

    def test_get_total_items(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)
        sl.add_item("butter", 200)

        self.assertEqual(sl.get_total_items(), 3)

    def test_get_total_quantity(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)
        sl.add_item("butter", 200)

        self.assertEqual(sl.get_total_quantity(), 950)

    def test_get_categorized_items(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)

        categories = sl.get_categorized_items()

        self.assertIn("uncategorized", categories)
        self.assertIn("flour", categories["uncategorized"])
        self.assertIn("sugar", categories["uncategorized"])

    def test_has_item(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)

        self.assertTrue(sl.has_item("flour"))
        self.assertFalse(sl.has_item("sugar"))

    def test_get_item_quantity(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)

        self.assertEqual(sl.get_item_quantity("flour"), 500)
        self.assertEqual(sl.get_item_quantity("nonexistent"), 0)

    def test_export(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)

        exported = sl.export()

        self.assertIsInstance(exported, dict)
        self.assertEqual(exported["flour"], 500)
        self.assertEqual(exported["sugar"], 250)

    def test_import_list(self):
        sl = ShoppingList()
        data = {"flour": 500, "sugar": 250}

        sl.import_list(data)

        self.assertEqual(sl.items["flour"], 500)
        self.assertEqual(sl.items["sugar"], 250)

    def test_merge(self):
        sl1 = ShoppingList()
        sl1.add_item("flour", 500)
        sl1.add_item("sugar", 250)

        sl2 = ShoppingList()
        sl2.add_item("butter", 200)
        sl2.add_item("flour", 300)

        merged = sl1.merge(sl2)

        self.assertEqual(merged.items["flour"], 800)
        self.assertEqual(merged.items["sugar"], 250)
        self.assertEqual(merged.items["butter"], 200)

    def test_scale_quantities(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)
        sl.add_item("sugar", 250)

        sl.scale_quantities(2)

        self.assertEqual(sl.items["flour"], 1000)
        self.assertEqual(sl.items["sugar"], 500)

        # Test zero factor
        sl.scale_quantities(0)
        self.assertEqual(sl.items["flour"], 0)
        self.assertEqual(sl.items["sugar"], 0)

    def test_scale_quantities_negative_factor(self):
        sl = ShoppingList()
        sl.add_item("flour", 500)

        with self.assertRaises(ValueError) as context:
            sl.scale_quantities(-1)

        self.assertTrue("Scale factor must be non-negative" in str(context.exception))
        self.assertEqual(sl.items["flour"], 500)

    def test_generate_shopping_list_from_mealplan():
        mp = MealPlan()
        mp.add_meal("Monday", Recipe("Breakfast", {"bread": 2, "cheese": 1}, 200, 10, 10, 20))
        mp.add_meal("Monday", Recipe("Lunch", {"bread": 1, "ham": 2}, 300, 20, 15, 30))

        sl = ShoppingList()
        sl.add_from_mealplan(mp)

        expected = {"bread": 3, "cheese": 1, "ham": 2}
        assert sl.get_items() == expected


if __name__ == "__main__":
    unittest.main()