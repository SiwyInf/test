from collections import defaultdict
from unittest.mock import patch
from typing import Dict, Union
from src.recipe import Recipe
from src.mealplan import MealPlan


def generate_shopping_list(recipes: list[Recipe]) -> Dict[str, float]:
    """Generates a shopping list from a list of recipes."""
    shopping_list = defaultdict(float)
    for recipe in recipes:
        for ingredient, quantity in recipe.ingredients.items():
            shopping_list[ingredient] += quantity
    return dict(shopping_list)


class ShoppingList:
    def __init__(self) -> None:
        """Initializes an empty shopping list."""
        self.items: defaultdict[str, float] = defaultdict(float)

    def add_item(self, ingredient: str, quantity: float) -> None:
        """Adds a specified quantity of an ingredient to the shopping list."""
        if quantity > 0:
            self.items[ingredient] += quantity

    def get_items(self) -> Dict[str, float]:
        """Returns the current items in the shopping list."""
        return dict(self.items)

    def add_from_recipe(self, recipe: Recipe) -> None:
        """Adds ingredients from a recipe to the shopping list."""
        for ingredient, quantity in recipe.ingredients.items():
            self.add_item(ingredient, quantity)

    def add_from_mealplan(self, mealplan: MealPlan) -> None:
        """Adds ingredients from all meals in a meal plan to the shopping list."""
        for day, meals in mealplan.plan.items():
            for meal in meals:
                if not isinstance(meal, Recipe):
                    raise TypeError(
                        f"meal must be an instance of Recipe, but got {type(meal)}"
                    )

                for ingredient, quantity in meal.ingredients.items():
                    self.add_item(ingredient, quantity)

    def filter_by_threshold(self, threshold: float) -> "ShoppingList":
        """Filters the shopping list to only include items with quantity above a certain threshold."""
        filtered = ShoppingList()
        for ingredient, quantity in self.items.items():
            if quantity >= threshold:
                filtered.add_item(ingredient, quantity)
        return filtered

    def remove_item(self, ingredient: str) -> None:
        """Removes an ingredient from the shopping list."""
        if ingredient in self.items:
            del self.items[ingredient]

    def clear(self) -> None:
        """Clears all items from the shopping list."""
        self.items.clear()

    def update_item_quantity(self, ingredient: str, quantity: float) -> None:
        """Updates the quantity of a specific ingredient."""
        if ingredient in self.items and quantity > 0:
            self.items[ingredient] = quantity

    def get_total_items(self) -> int:
        """Returns the total number of unique items in the shopping list."""
        return len(self.items)

    def get_total_quantity(self) -> float:
        """Returns the total quantity of all items in the shopping list."""
        return sum(self.items.values())

    def get_categorized_items(self) -> Dict[str, Dict[str, float]]:
        """Returns the shopping list categorized by ingredients' category."""
        categories: defaultdict[str, Dict[str, float]] = defaultdict(dict)
        for ingredient, quantity in self.items.items():
            category = (
                "uncategorized"  # Add your logic to categorize ingredients if necessary
            )
            categories[category][ingredient] = quantity
        return dict(categories)

    def has_item(self, ingredient: str) -> bool:
        """Checks if a particular ingredient is in the shopping list."""
        return ingredient in self.items

    def get_item_quantity(self, ingredient: str) -> float:
        """Returns the quantity of a specific ingredient."""
        return self.items.get(ingredient, 0)

    def export(self) -> Dict[str, float]:
        """Exports the shopping list as a dictionary."""
        return dict(self.items)

    def import_list(self, data: Dict[str, float]) -> None:
        """Imports a shopping list from a dictionary."""
        self.items = defaultdict(float, data)

    def merge(self, other: "ShoppingList") -> "ShoppingList":
        """Merges another shopping list into the current one."""
        merged = ShoppingList()
        merged.items.update(self.items)
        for ingredient, quantity in other.items.items():
            merged.add_item(ingredient, quantity)
        return merged

    def scale_quantities(self, factor: float) -> None:
        """Scales the quantities of all ingredients in the shopping list by a factor."""
        if factor < 0:
            raise ValueError("Scale factor must be non-negative.")
        for ingredient in self.items:
            self.items[ingredient] *= factor


def test_daily_summary_with_mocked_nutrients():
    """Test sprawdza, czy daily_summary poprawnie sumuje wartości odżywcze (z mockiem)."""
    # Tworzymy mocka dla metody total_nutrients()
    with patch.object(Recipe, 'total_nutrients', autospec=True) as mock_nutrients:
        # Konfigurujemy mocka, aby zwracał stałe wartości
        mock_nutrients.return_value = {"kcal": 100, "protein": 10, "fat": 5, "carbs": 20}

        plan = MealPlan()
        fake_recipe = Recipe("Fake", {}, 0, 0, 0, 0)  # Dane nieistotne, bo mock nadpisuje

        plan.add_meal("Monday", fake_recipe)
        summary = plan.daily_summary("Monday")

        # Sprawdzamy, czy metoda została wywołana
        mock_nutrients.assert_called_once()
        # Sprawdzamy, czy podsumowanie jest zgodne z mockiem
        assert summary == {"kcal": 100, "protein": 10, "fat": 5, "carbs": 20}