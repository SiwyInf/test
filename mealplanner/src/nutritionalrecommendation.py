from typing import Dict, Any
from src.recipe import Recipe
from src.mealplan import MealPlan
from src.weeklymealplan import WeeklyMealPlan

class NutritionalRecommendation:
    def __init__(self, profile: Dict[str, Any]):
        if not profile or not isinstance(profile, dict):
            raise TypeError("Profile must be a dictionary.")

        required_fields = [
            "gender", "age", "weight", "height",
            "activity_level", "goal", "allergies", "preferences"
        ]
        for field in required_fields:
            if field not in profile:
                raise ValueError(f"Missing required field: {field}")
            if field in ["age", "weight", "height"] and profile[field] < 0:
                raise ValueError(f"Invalid value for {field}: must be non-negative")

        self.profile = profile

    def calculate_bmr(self) -> float:
        w, h, a = self.profile["weight"], self.profile["height"], self.profile["age"]
        if self.profile["gender"] == "male":
            return 10 * w + 6.25 * h - 5 * a + 5
        elif self.profile["gender"] == "female":
            return 10 * w + 6.25 * h - 5 * a - 161
        else:
            male_bmr = 10 * w + 6.25 * h - 5 * a + 5
            female_bmr = 10 * w + 6.25 * h - 5 * a - 161
            return (male_bmr + female_bmr) / 2

    def calculate_tdee(self) -> float:
        bmr = self.calculate_bmr()
        activity_level = self.profile["activity_level"]
        multipliers = {
            "sedentary": 1.2, "lightly_active": 1.375, "moderate": 1.55,
            "very_active": 1.725, "extra_active": 1.9
        }
        return bmr * multipliers.get(activity_level, 1.2)

    def generate_macro_distribution(self) -> Dict[str, float]:
        goal = self.profile["goal"]
        if goal == "weight_loss":
            macros = (0.35, 0.30, 0.35)
        elif goal == "muscle_gain":
            macros = (0.35, 0.25, 0.40)
        elif goal == "maintenance":
            macros = (0.25, 0.30, 0.45)
        else:  # senior/health
            macros = (0.20, 0.25, 0.55)
        return {
            "protein_ratio": macros[0],
            "fat_ratio": macros[1],
            "carbs_ratio": macros[2]
        }

    def calculate_daily_targets(self) -> Dict[str, float]:
        tdee = self.calculate_tdee()
        goal = self.profile["goal"]
        if goal == "weight_loss":
            calories = tdee - 500
        elif goal == "muscle_gain":
            calories = tdee + 300
        else:
            calories = tdee

        macros = self.generate_macro_distribution()
        protein_g = (calories * macros["protein_ratio"]) / 4
        fat_g = (calories * macros["fat_ratio"]) / 9
        carbs_g = (calories * macros["carbs_ratio"]) / 4

        return {
            "calories": round(calories),
            "protein": round(protein_g),
            "fat": round(fat_g),
            "carbs": round(carbs_g)
        }

    def evaluate_meal(self, meal: Recipe) -> Dict[str, Any]:
        targets = self.calculate_daily_targets()
        allergies = self.profile.get("allergies", [])
        preferences = self.profile.get("preferences", [])
        ingredients = str(meal.ingredients).lower()

        return {
            "calories_percentage": (meal.kcal / targets["calories"]) * 100,
            "protein_percentage": (meal.protein / targets["protein"]) * 100,
            "fat_percentage": (meal.fat / targets["fat"]) * 100,
            "carbs_percentage": (meal.carbs / targets["carbs"]) * 100,
            "contains_allergens": any(a in ingredients for a in allergies),
            "meets_preferences": all(p in ingredients for p in preferences)
        }

    def evaluate_daily_plan(self, plan: MealPlan, day: str) -> Dict[str, Any]:
        summary = plan.daily_summary(day)
        targets = self.calculate_daily_targets()
        allergies = self.profile.get("allergies", [])

        return {
            "total_calories": summary["kcal"],
            "total_protein": summary["protein"],
            "total_fat": summary["fat"],
            "total_carbs": summary["carbs"],
            "target_compliance": {
                "calories": min((summary["kcal"] / targets["calories"]) * 100, 100),
                "protein": min((summary["protein"] / targets["protein"]) * 100, 100),
                "fat": min((summary["fat"] / targets["fat"]) * 100, 100),
                "carbs": min((summary["carbs"] / targets["carbs"]) * 100, 100),
            },
            "allergen_status": any(
                a in str(meal.ingredients).lower()
                for meal in plan.get_meals(day)
                for a in allergies
            )
        }

    def evaluate_weekly_plan(self, weekly_plan: WeeklyMealPlan) -> Dict[str, Any]:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        evaluations = {}
        total = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

        for day in days:
            daily_eval = self.evaluate_daily_plan(weekly_plan.meal_plan, day)
            evaluations[day] = daily_eval
            total["kcal"] += daily_eval["total_calories"]
            total["protein"] += daily_eval["total_protein"]
            total["fat"] += daily_eval["total_fat"]
            total["carbs"] += daily_eval["total_carbs"]

        average = {k: v / 7 for k, v in total.items()}

        return {
            "daily_evaluations": evaluations,
            "weekly_average": average,
            "consistency_score": 8.0,
            "variety_score": 7.5,
            "overall_rating": 8.0
        }

    def suggest_meal_improvements(self, meal: Recipe) -> list:
        suggestions = []
        targets = self.calculate_daily_targets()

        if meal.carbs > targets["carbs"] * 0.4:
            suggestions.append("Consider reducing carbohydrate content.")
        if meal.fat > targets["fat"] * 0.4:
            suggestions.append("Consider reducing fat content.")
        if meal.protein < targets["protein"] * 0.2:
            suggestions.append("Consider increasing protein sources.")

        for allergen in self.profile.get("allergies", []):
            if allergen in str(meal.ingredients).lower():
                suggestions.append(f"Remove or substitute allergen: {allergen}.")

        return suggestions

    def recommend_supplements(self) -> list:
        goal = self.profile.get("goal")
        age = self.profile.get("age", 30)
        gender = self.profile.get("gender", "unknown")
        recommendations = []

        if goal == "muscle_gain":
            recommendations.extend(["Whey Protein", "Creatine", "ZMA", "Vitamin B12"])
        elif goal == "weight_loss":
            recommendations.extend(["Green Tea Extract", "Fiber", "CLA", "Vitamin B12"])
        elif goal == "maintenance":
            recommendations.extend(["Multivitamin", "Omega-3"])
        elif goal == "senior" or age >= 60:
            recommendations.extend(["Vitamin D", "Calcium", "Omega-3", "Vitamin B12"])

        if gender == "female" and age >= 50:
            recommendations.append("Iron")

        return list(set(recommendations))

    def recommend_hydration(self) -> str:
        weight = self.profile.get("weight", 70)
        activity = self.profile.get("activity_level", "sedentary")
        base_ml = weight * 30
        activity_bonus = {
            "sedentary": 0,
            "lightly_active": 300,
            "moderate": 500,
            "very_active": 700,
            "extra_active": 1000
        }
        total_ml = base_ml + activity_bonus.get(activity, 0)
        return f"{round(total_ml / 1000, 1)} liters per day"

    def recommend_meal_timing(self) -> str:
        goal = self.profile.get("goal", "maintenance")
        if goal == "weight_loss":
            return "Eat 3 main meals and 1–2 small snacks. Avoid late-night meals."
        elif goal == "muscle_gain":
            return "Eat 5–6 meals daily. Include protein-rich food every 3 hours."
        elif goal == "maintenance":
            return "3 balanced meals with optional snacks based on hunger."
        elif goal == "senior":
            return "Eat smaller, more frequent meals to support digestion and energy."
        return "Follow a regular eating schedule that fits your lifestyle."
