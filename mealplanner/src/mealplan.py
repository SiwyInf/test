from typing import Dict, List
from src.recipe import Recipe  # Poprawiony import

class MealPlan:
    def __init__(self) -> None:
        self.plan: Dict[str, List[Recipe]] = {
            day: [] for day in [
                "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"
            ]
        }

    def add_meal(self, day: str, meal: Recipe) -> None:
        if not isinstance(meal, Recipe):
            raise TypeError("meal must be an instance of Recipe")
        if day not in self.plan:
            raise ValueError("Invalid day")
        self.plan[day].append(meal)

    def daily_summary(self, day: str) -> Dict[str, int]:
        if day not in self.plan:
            raise ValueError("Invalid day")
        total: Dict[str, int] = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
        for recipe in self.plan[day]:
            nutrients = recipe.total_nutrients()
            for key in total:
                total[key] += nutrients.get(key, 0)
        return total

    def get_meals(self, day: str) -> List[Recipe]:
        if day not in self.plan:
            raise ValueError("Invalid day")
        return self.plan[day]
