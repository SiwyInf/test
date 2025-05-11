import unittest
from src.recipe import Recipe


class TestRecipe(unittest.TestCase):
    """Tests for the Recipe class using unittest framework"""

    def test_valid_recipe_smoothie(self):
        """Test correct creation of smoothie recipe with nutrition validation"""
        r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 180)
        self.assertEqual(nutrients["protein"], 5)
        self.assertEqual(nutrients["fat"], 3)
        self.assertEqual(nutrients["carbs"], 35)

    def test_valid_recipe_soup(self):
        """Test correct creation of soup recipe with nutrition validation"""
        r = Recipe("Soup", {"water": 500, "carrot": 100}, 90, 2, 1, 10)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 90)
        self.assertEqual(nutrients["protein"], 2)
        self.assertEqual(nutrients["fat"], 1)
        self.assertEqual(nutrients["carbs"], 10)

    def test_valid_recipe_rice(self):
        """Test correct creation of rice recipe with nutrition validation"""
        r = Recipe("Rice", {"rice": 100}, 130, 3, 1, 30)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 130)
        self.assertEqual(nutrients["protein"], 3)
        self.assertEqual(nutrients["fat"], 1)
        self.assertEqual(nutrients["carbs"], 30)

    def test_valid_recipe_omelette(self):
        """Test correct creation of omelette recipe with nutrition validation"""
        r = Recipe("Omelette", {"eggs": 2, "cheese": 50}, 250, 15, 20, 2)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 250)
        self.assertEqual(nutrients["protein"], 15)
        self.assertEqual(nutrients["fat"], 20)
        self.assertEqual(nutrients["carbs"], 2)

    def test_valid_recipe_pancakes(self):
        """Test correct creation of pancakes recipe with nutrition validation"""
        r = Recipe("Pancakes", {"flour": 100, "milk": 200}, 300, 7, 6, 40)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 300)
        self.assertEqual(nutrients["protein"], 7)
        self.assertEqual(nutrients["fat"], 6)
        self.assertEqual(nutrients["carbs"], 40)

    def test_invalid_recipe_empty_name(self):
        """Test that an empty recipe name raises ValueError"""
        with self.assertRaises(ValueError):
            Recipe("", {}, 100, 5, 5, 5)

    def test_invalid_recipe_negative_kcal(self):
        """Test that negative calories raises ValueError"""
        with self.assertRaises(ValueError):
            Recipe("Invalid", {}, -10, 5, 5, 5)

    def test_invalid_recipe_negative_protein(self):
        """Test that negative protein raises ValueError"""
        with self.assertRaises(ValueError):
            Recipe("Invalid", {}, 100, -5, 5, 5)

    def test_invalid_recipe_negative_fat(self):
        """Test that negative fat raises ValueError"""
        with self.assertRaises(ValueError):
            Recipe("Invalid", {}, 100, 5, -5, 5)

    def test_invalid_recipe_negative_carbs(self):
        """Test that negative carbs raises ValueError"""
        with self.assertRaises(ValueError):
            Recipe("Invalid", {}, 100, 5, 5, -5)

    def test_large_values_recipe(self):
        """Test recipes with large nutritional values"""
        r = Recipe("Mega Meal", {"meat": 1000, "rice": 500}, 10000, 500, 200, 600)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 10000)
        self.assertEqual(nutrients["protein"], 500)
        self.assertEqual(nutrients["fat"], 200)
        self.assertEqual(nutrients["carbs"], 600)

    def test_very_large_values_recipe(self):
        """Test recipes with very large nutritional values"""
        r = Recipe("Ultra Meal", {"meat": 10000, "rice": 5000}, 100000, 5000, 2000, 6000)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 100000)
        self.assertEqual(nutrients["protein"], 5000)
        self.assertEqual(nutrients["fat"], 2000)
        self.assertEqual(nutrients["carbs"], 6000)

    def test_negative_ingredient_quantity(self):
        """Test that negative ingredient quantity raises ValueError"""
        with self.assertRaisesRegex(ValueError, "Ingredient quantity for 'milk' cannot be negative"):
            Recipe("Strange", {"milk": -200}, 100, 5, 5, 5)

    def test_very_long_name(self):
        """Test recipes with very long names"""
        name = "A" * 1000  # very long name
        r = Recipe(name, {"air": 0}, 0, 0, 0, 0)
        self.assertEqual(r.name, name)

    def test_zero_ingredient_quantity(self):
        """Test recipes with zero ingredient quantity"""
        r = Recipe("ZeroFood", {"water": 0}, 0, 0, 0, 0)
        self.assertEqual(r.ingredients["water"], 0)

    def test_recipe_with_zero_values_everywhere(self):
        """Test recipes with all zero nutritional values"""
        r = Recipe("ZeroMeal", {}, 0, 0, 0, 0)
        self.assertEqual(r.total_nutrients(), {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0})

    def test_recipe_with_mixed_units(self):
        """Test recipes with mixed units in ingredient names"""
        r = Recipe("Mixed", {"rice (g)": 100, "milk (ml)": 200}, 350, 15, 10, 40)
        self.assertIn("milk (ml)", r.ingredients)

    def test_recipe_str_name_is_preserved(self):
        """Test that special characters in recipe names are preserved"""
        name = "Śniadanie #1 -- 🍳🥓"
        r = Recipe(name, {"jajko": 1}, 120, 10, 8, 1)
        self.assertEqual(r.name, name)

    def test_recipe_zero_protein_meal(self):
        """Test recipes with zero protein"""
        r = Recipe("Woda", {"woda": 200}, 0, 0, 0, 0)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["protein"], 0)

    def test_very_large_quantity(self):
        """Test recipes with very large ingredient quantities"""
        r = Recipe("LargeFlour", {"mąka": 99999}, 100, 1, 1, 1)
        self.assertEqual(r.ingredients["mąka"], 99999)

    def test_polish_chars_name(self):
        """Test recipes with Polish characters in the name"""
        r = Recipe("Śniadanie", {"x": 1}, 100, 1, 1, 1)
        self.assertEqual(r.name, "Śniadanie")

    def test_name_with_special_chars(self):
        """Test recipes with special characters in the name"""
        r = Recipe("lunch@12", {"x": 1}, 100, 1, 1, 1)
        self.assertEqual(r.name, "lunch@12")

    def test_name_with_underscore(self):
        """Test recipes with underscores in the name"""
        r = Recipe("kolacja_3", {"x": 1}, 100, 1, 1, 1)
        self.assertEqual(r.name, "kolacja_3")

    def test_name_with_emoji(self):
        """Test recipes with emoji in the name"""
        r = Recipe("🍏🍎🍐🍊", {"x": 1}, 100, 1, 1, 1)
        self.assertEqual(r.name, "🍏🍎🍐🍊")

    def test_ingredient_keys_are_not_strings(self):
        """Test recipes with non-string keys in ingredient dictionary"""
        r = Recipe("NumericKeys", {1: 100, 2.5: 50}, 100, 1, 1, 1)
        self.assertEqual(r.ingredients[1], 100)
        self.assertEqual(r.ingredients[2.5], 50)

    def test_recipe_with_none_ingredient_dict(self):
        """Test that None as ingredient dictionary raises TypeError"""
        with self.assertRaises(TypeError):
            Recipe("NoneIngredients", None, 100, 5, 5, 5)

    def test_recipe_str_representation(self):
        """Test string representation of recipes"""
        r = Recipe("NiceMeal", {"pasta": 200}, 300, 10, 5, 50)
        self.assertIn("NiceMeal", str(r))

    def test_recipe_with_multiple_ingredients(self):
        """Test recipes with multiple ingredients"""
        r = Recipe(
            "ComplexMeal", {"rice": 100, "chicken": 150, "sauce": 50}, 450, 30, 15, 40
        )
        self.assertEqual(len(r.ingredients), 3)
        self.assertEqual(r.ingredients["rice"], 100)
        self.assertEqual(r.ingredients["chicken"], 150)
        self.assertEqual(r.ingredients["sauce"], 50)

    def test_recipe_with_maximum_values(self):
        """Test recipes with maximum integer values"""
        r = Recipe("MaxMeal", {"ingredient": 1}, 2**31 - 1, 2**31 - 1, 2**31 - 1, 2**31 - 1)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], 2**31 - 1)
        self.assertEqual(nutrients["protein"], 2**31 - 1)

    def test_recipe_ingredient_with_decimal_value(self):
        """Test recipes with decimal values in ingredient quantities"""
        r = Recipe("PreciseRecipe", {"flour": 123.456}, 200, 5, 3, 30)
        self.assertEqual(r.ingredients["flour"], 123.456)

    def test_recipe_with_special_chars_in_ingredients(self):
        """Test recipes with special characters in ingredient names"""
        r = Recipe("SpecialIngredients", {"$pec!al": 100, "normal": 200}, 300, 10, 5, 40)
        self.assertEqual(r.ingredients["$pec!al"], 100)

    def test_recipe_with_unicode_ingredient_names(self):
        """Test recipes with Unicode characters in ingredient names"""
        r = Recipe("UnicodeIngredients", {"śliwki": 10, "jabłka": 5}, 150, 2, 1, 30)
        self.assertEqual(r.ingredients["śliwki"], 10)
        self.assertEqual(r.ingredients["jabłka"], 5)

    def test_recipe_nutritional_values_consistency(self):
        """Test consistency between total_nutrients() method and class attributes"""
        r = Recipe("TestConsistency", {"test": 100}, 200, 10, 5, 25)
        nutrients = r.total_nutrients()
        self.assertEqual(nutrients["kcal"], r.kcal)
        self.assertEqual(nutrients["protein"], r.protein)
        self.assertEqual(nutrients["fat"], r.fat)
        self.assertEqual(nutrients["carbs"], r.carbs)

    def test_recipe_with_ingredient_quantity_one(self):
        """Test recipes with ingredient quantity of 1"""
        r = Recipe("SingleUnit", {"egg": 1}, 80, 6, 5, 0)
        self.assertEqual(r.ingredients["egg"], 1)

    def test_recipe_max_name_length(self):
        """Test recipes with maximum name length"""
        long_name = "X" * 10000  # Very long name
        r = Recipe(long_name, {"x": 1}, 100, 5, 5, 5)
        self.assertEqual(r.name, long_name)

    def test_recipe_with_boolean_ingredient_keys(self):
        """Test recipes with boolean keys in ingredient dictionary"""
        r = Recipe("BoolKeys", {True: 100, False: 50}, 150, 5, 5, 5)
        self.assertEqual(r.ingredients[True], 100)
        self.assertEqual(r.ingredients[False], 50)

    def test_recipe_with_tuple_ingredient_keys(self):
        """Test recipes with tuple keys in ingredient dictionary"""
        r = Recipe(
            "TupleKeys", {("apple", "fresh"): 3, ("banana", "ripe"): 2}, 200, 5, 2, 30
        )
        self.assertEqual(r.ingredients[("apple", "fresh")], 3)
        self.assertEqual(r.ingredients[("banana", "ripe")], 2)


if __name__ == "__main__":
    unittest.main()