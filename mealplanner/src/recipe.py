from unittest.mock import patch
import pytest
from typing import Dict


class Recipe:
    def __init__(
        self,
        name: str,
        ingredients: Dict[str, float],
        kcal: float,
        protein: float,
        fat: float,
        carbs: float,
    ):
        if not name:
            raise ValueError("Recipe name cannot be empty")
        if kcal < 0 or protein < 0 or fat < 0 or carbs < 0:
            raise ValueError("Nutritional values cannot be negative")
        if ingredients is None:
            raise TypeError("Ingredients cannot be None")

        for ingredient, quantity in ingredients.items():
            if quantity < 0:
                raise ValueError(
                    f"Ingredient quantity for '{ingredient}' cannot be negative"
                )

        self.name = name
        self.ingredients = ingredients
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs

    def total_nutrients(self) -> Dict[str, float]:
        return {
            "kcal": self.kcal,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs,
        }

    def __str__(self) -> str:
        ingredient_list = ", ".join(
            f"{ingredient}: {quantity}"
            for ingredient, quantity in self.ingredients.items()
        )
        return f"{self.name} ({ingredient_list})"

    # 1. Methods to modify ingredients:

    def add_ingredient(self, name: str, quantity: float) -> None:
        if quantity < 0:
            raise ValueError("Ingredient quantity cannot be negative")
        self.ingredients[name] = quantity

    def remove_ingredient(self, name: str) -> None:
        if name in self.ingredients:
            del self.ingredients[name]

    def update_ingredient_quantity(self, name: str, new_quantity: float) -> None:
        if name not in self.ingredients:
            raise ValueError(f"Ingredient '{name}' not found")
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.ingredients[name] = new_quantity

    # 2. Methods to update nutritional values:

    def update_kcal(self, new_kcal: float) -> None:
        if new_kcal < 0:
            raise ValueError("kcal cannot be negative")
        self.kcal = new_kcal

    def update_protein(self, new_protein: float) -> None:
        if new_protein < 0:
            raise ValueError("Protein cannot be negative")
        self.protein = new_protein

    def update_fat(self, new_fat: float) -> None:
        if new_fat < 0:
            raise ValueError("Fat cannot be negative")
        self.fat = new_fat

    def update_carbs(self, new_carbs: float) -> None:
        if new_carbs < 0:
            raise ValueError("Carbs cannot be negative")
        self.carbs = new_carbs

    # 3. Helper methods:

    def contains_ingredient(self, name: str) -> bool:
        return name in self.ingredients

    def total_weight(self) -> float:
        return sum(self.ingredients.values())

    def scale_recipe(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("Scaling factor must be positive")
        for ingredient in self.ingredients:
            self.ingredients[ingredient] *= factor
        self.kcal *= factor
        self.protein *= factor
        self.fat *= factor
        self.carbs *= factor

    # 4. Methods to compare recipes:

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Recipe):
            return False
        return (
            self.name == other.name
            and self.ingredients == other.ingredients
            and self.kcal == other.kcal
            and self.protein == other.protein
            and self.fat == other.fat
            and self.carbs == other.carbs
        )

    # 5. Methods for text representation:

    def detailed_str(self) -> str:
        ingredients = "\n".join(
            f"- {name}: {quantity}g" for name, quantity in self.ingredients.items()
        )
        nutrients = self.total_nutrients()
        return (
            f"Recipe: {self.name}\n"
            f"Ingredients:\n{ingredients}\n"
            f"Nutrition per serving:\n"
            f"- kcal: {nutrients['kcal']}\n"
            f"- protein: {nutrients['protein']}g\n"
            f"- fat: {nutrients['fat']}g\n"
            f"- carbs: {nutrients['carbs']}g"
        )

    # 6. Method to split the recipe into portions:

    def split_into_portions(self, portions: int) -> "Recipe":
        if portions <= 0:
            raise ValueError("Number of portions must be positive")
        factor = 1 / portions
        new_ingredients = {name: qty * factor for name, qty in self.ingredients.items()}
        return Recipe(
            name=f"{self.name} (1/{portions} portion)",
            ingredients=new_ingredients,
            kcal=self.kcal * factor,
            protein=self.protein * factor,
            fat=self.fat * factor,
            carbs=self.carbs * factor,
        )

    # 7. Mock

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