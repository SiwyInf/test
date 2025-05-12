from typing import Dict, List
from src.recipe import Recipe


class MealPlan:
    def __init__(self) -> None:
        self.plan: Dict[str, List[Recipe]] = {
            day: []
            for day in [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        }

    def add_meal(self, day: str, meal: Recipe) -> None:
        if not isinstance(meal, Recipe):
            raise TypeError("meal must be an instance of Recipe")

        if day not in self.plan:
            raise ValueError("Invalid day")

        self.plan[day].append(meal)

    def remove_meal(self, day: str, meal: Recipe) -> None:
        """Removes a meal from a specific day."""
        if day not in self.plan:
            raise ValueError("Invalid day")

        try:
            self.plan[day].remove(meal)
        except ValueError:
            raise ValueError("Meal not found on the specified day")

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
        """Returns all meals for a given day."""
        return self.plan.get(day, [])

    def clear_day(self, day: str) -> None:
        """Clears all meals from a specific day."""
        self.plan[day] = []

    def weekly_summary(self) -> Dict[str, Dict[str, int]]:
        """Returns a summary of nutrients for the entire week."""
        weekly_total: Dict[str, Dict[str, int]] = {
            "Monday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
            "Tuesday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
            "Wednesday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
            "Thursday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
            "Friday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
            "Saturday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
            "Sunday": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
        }

        for day, meals in self.plan.items():
            for recipe in meals:
                nutrients = recipe.total_nutrients()
                for key in weekly_total[day]:
                    weekly_total[day][key] += nutrients.get(key, 0)

        return weekly_total
