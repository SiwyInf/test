from src.mealplan import MealPlan
from src.recipe import Recipe
from typing import Dict, List, Optional, Union


class WeeklyMealPlan:
    """
    Class for managing weekly meal plans with additional functionality
    beyond the basic MealPlan class.
    """

    def __init__(self, meal_plan: Optional[MealPlan] = None):
        """
        Initialize a WeeklyMealPlan with an existing MealPlan or create a new one.

        Args:
            meal_plan: Optional MealPlan object to start with
        """
        if meal_plan is not None:
            self.meal_plan = meal_plan
        else:
            self.meal_plan = MealPlan()

    def add_meal(self, day: str, recipe: Recipe) -> None:
        """
        Add a meal to a specific day in the weekly plan.

        Args:
            day: Day of the week to add the meal to
            recipe: Recipe object to add

        Raises:
            ValueError: If day is not valid
            TypeError: If recipe is not a Recipe object
        """
        self.meal_plan.add_meal(day, recipe)

    def weekly_summary(self) -> Dict[str, int]:
        """
        Calculate total nutritional values for the entire week.

        Returns:
            Dictionary with total kcal, protein, fat, and carbs for the week
        """
        summary = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

        for day in self.meal_plan.plan.keys():
            day_summary = self.meal_plan.daily_summary(day)
            summary["kcal"] += day_summary["kcal"]
            summary["protein"] += day_summary["protein"]
            summary["fat"] += day_summary["fat"]
            summary["carbs"] += day_summary["carbs"]

        return summary

    def daily_average(self) -> Dict[str, int]:
        """
        Calculate average daily nutritional values from the weekly summary.

        Returns:
            Dictionary with average daily kcal, protein, fat, and carbs
        """
        weekly_totals = self.weekly_summary()
        days_count = 7  # Always 7 days in a week

        return {
            "kcal": round(weekly_totals["kcal"] / days_count),
            "protein": round(weekly_totals["protein"] / days_count),
            "fat": round(weekly_totals["fat"] / days_count),
            "carbs": round(weekly_totals["carbs"] / days_count)
        }

    def generate_shopping_list(self) -> Dict[str, Union[int, float]]:
        """
        Generate a shopping list based on all recipes in the weekly plan.

        Returns:
            Dictionary with ingredients as keys and total quantities as values
        """
        shopping_list = {}

        for day, meals in self.meal_plan.plan.items():
            for meal in meals:
                for ingredient, quantity in meal.ingredients.items():
                    if ingredient in shopping_list:
                        shopping_list[ingredient] += quantity
                    else:
                        shopping_list[ingredient] = quantity

        return shopping_list

    def get_unique_recipes(self) -> List[Recipe]:
        """
        Get a list of unique recipes used in the weekly plan.

        Returns:
            List of unique Recipe objects in the plan
        """
        unique_recipes = set()

        for day, meals in self.meal_plan.plan.items():
            for meal in meals:
                unique_recipes.add(meal)

        return list(unique_recipes)

    def count_recipes_by_day(self) -> Dict[str, int]:
        """
        Count the number of meals for each day in the plan.

        Returns:
            Dictionary with days as keys and meal counts as values
        """
        counts = {}

        for day, meals in self.meal_plan.plan.items():
            counts[day] = len(meals)

        return counts

    def get_meal_variety(self) -> float:
        """
        Calculate meal variety as the ratio of unique recipes to total recipes.

        Returns:
            Float between 0 and 1 representing meal variety
        """
        total_meals = sum(len(meals) for meals in self.meal_plan.plan.values())
        if total_meals == 0:
            return 0.0

        unique_meals = len(self.get_unique_recipes())
        return unique_meals / total_meals

    def compare_daily_nutrition(self, day1: str, day2: str) -> Dict[str, float]:
        """
        Compare nutritional values between two days.

        Args:
            day1: First day to compare
            day2: Second day to compare

        Returns:
            Dictionary with differences in nutritional values

        Raises:
            ValueError: If either day is not valid
        """
        summary1 = self.meal_plan.daily_summary(day1)
        summary2 = self.meal_plan.daily_summary(day2)

        return {
            "kcal_diff": summary2["kcal"] - summary1["kcal"],
            "protein_diff": summary2["protein"] - summary1["protein"],
            "fat_diff": summary2["fat"] - summary1["fat"],
            "carbs_diff": summary2["carbs"] - summary1["carbs"]
        }

    def get_day_with_highest_calories(self) -> str:
        """
        Find the day with the highest caloric intake.

        Returns:
            Day of the week with highest calories
        """
        max_calories = -1
        max_day = None

        for day in self.meal_plan.plan.keys():
            calories = self.meal_plan.daily_summary(day)["kcal"]
            if calories > max_calories:
                max_calories = calories
                max_day = day

        return max_day or "No meals found"

    def get_day_with_highest_protein(self) -> str:
        """
        Find the day with the highest protein intake.

        Returns:
            Day of the week with highest protein
        """
        max_protein = -1
        max_day = None

        for day in self.meal_plan.plan.keys():
            protein = self.meal_plan.daily_summary(day)["protein"]
            if protein > max_protein:
                max_protein = protein
                max_day = day

        return max_day or "No meals found"

    def calculate_balance_score(self) -> float:
        """
        Calculate a 'balance score' for the week's meal plan.
        Higher is better, with a max of 10.0.

        Returns:
            Score from 0 to 10
        """
        # Get daily averages
        avg = self.daily_average()

        # Calculate ratio of macros (protein:fat:carbs)
        total_macros = avg["protein"] + avg["fat"] + avg["carbs"]
        if total_macros == 0:
            return 0.0

        protein_ratio = avg["protein"] / total_macros
        fat_ratio = avg["fat"] / total_macros
        carbs_ratio = avg["carbs"] / total_macros

        # Ideal macro ratios (example): 0.3 protein, 0.3 fat, 0.4 carbs
        ideal_protein = 0.3
        ideal_fat = 0.3
        ideal_carbs = 0.4

        # Calculate deviations from ideal
        deviation = abs(protein_ratio - ideal_protein) + abs(fat_ratio - ideal_fat) + abs(carbs_ratio - ideal_carbs)

        # Convert deviation into a score out of 10 (lower deviation = higher score)
        score = max(0.0, 10.0 - deviation * 30)  # scale deviation (0.0 = perfect, 0.33+ = poor)
        return round(score, 2)
