from typing import Dict


class Recipe:
    def __init__(
        self,
        name: str,
        ingredients: Dict[str, float],
        kcal: int,
        protein: int,
        fat: int,
        carbs: int,
    ) -> None:
        if not name or kcal < 0 or protein < 0 or fat < 0 or carbs < 0:
            raise ValueError("Invalid nutritional values or name")

        if ingredients is None:
            raise TypeError("Ingredients cannot be None")

        for ingredient, quantity in ingredients.items():
            if quantity < 0:
                raise ValueError(f"Ingredient quantity for '{ingredient}' cannot be negative")

        self.name: str = name
        self.ingredients: Dict[str, float] = ingredients
        self.kcal: int = kcal
        self.protein: int = protein
        self.fat: int = fat
        self.carbs: int = carbs

    def total_nutrients(self) -> Dict[str, int]:
        return {
            "kcal": self.kcal,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs,
        }

    def __str__(self) -> str:
        return (
            f"Recipe(name={self.name}, kcal={self.kcal}, "
            f"protein={self.protein}, fat={self.fat}, carbs={self.carbs})"
        )
