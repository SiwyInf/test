from collections import defaultdict
from typing import Dict, List
from src.recipe import Recipe
from src.mealplan import MealPlan


def generate_shopping_list(recipes: List[Recipe]) -> Dict[str, float]:
    shopping_list = defaultdict(float)
    for recipe in recipes:
        for ingredient, quantity in recipe.ingredients.items():
            shopping_list[ingredient] += quantity
    return dict(shopping_list)


class ShoppingList:
    def __init__(self) -> None:
        self.items: Dict[str, float] = defaultdict(float)

    def add_item(self, ingredient: str, quantity: float) -> None:
        if quantity > 0:
            self.items[ingredient] += quantity

    def get_items(self) -> Dict[str, float]:
        return dict(self.items)

    def add_from_recipe(self, recipe: Recipe) -> None:
        for ingredient, quantity in recipe.ingredients.items():
            self.add_item(ingredient, quantity)

    def add_from_mealplan(self, meal_plan: MealPlan) -> None:
        for meals in meal_plan.plan.values():
            for recipe in meals:
                self.add_from_recipe(recipe)

    def filter_by_threshold(self, threshold: float) -> 'ShoppingList':
        filtered = ShoppingList()
        for ingredient, quantity in self.items.items():
            if quantity >= threshold:
                filtered.add_item(ingredient, quantity)
        return filtered

    def remove_item(self, ingredient: str) -> None:
        if ingredient in self.items:
            del self.items[ingredient]

    def clear(self) -> None:
        self.items.clear()

    def update_item_quantity(self, ingredient: str, quantity: float) -> None:
        if ingredient in self.items and quantity > 0:
            self.items[ingredient] = quantity

    def get_total_items(self) -> int:
        return len(self.items)

    def get_total_quantity(self) -> float:
        return sum(self.items.values())

    def get_categorized_items(self) -> Dict[str, Dict[str, float]]:
        categories = defaultdict(dict)
        for ingredient, quantity in self.items.items():
            category = "uncategorized"  # Można rozbudować w przyszłości
            categories[category][ingredient] = quantity
        return dict(categories)

    def has_item(self, ingredient: str) -> bool:
        return ingredient in self.items

    def get_item_quantity(self, ingredient: str) -> float:
        return self.items.get(ingredient, 0.0)

    def export(self) -> Dict[str, float]:
        return dict(self.items)

    def import_list(self, data: Dict[str, float]) -> None:
        self.items = defaultdict(float, data)

    def merge(self, other: 'ShoppingList') -> 'ShoppingList':
        merged = ShoppingList()
        merged.items.update(self.items)
        for ingredient, quantity in other.items.items():
            merged.add_item(ingredient, quantity)
        return merged

    def scale_quantities(self, factor: float) -> None:
        if factor < 0:
            raise ValueError("Scale factor must be non-negative.")
        for ingredient in self.items:
            self.items[ingredient] *= factor
