import unittest
from src.mealplan import MealPlan
from src.recipe import Recipe


class TestMealPlan(unittest.TestCase):
    def setUp(self):
        """Create a basic recipe that can be used in multiple tests"""
        self.basic_recipe = Recipe("Toast", {"bread": 2}, 150, 5, 2, 20)

    def test_add_meal_and_summary_for_each_day(self):
        """Test adding meals to plan for each day of the week and check daily summary"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            with self.subTest(day=day):
                plan = MealPlan()
                plan.add_meal(day, self.basic_recipe)
                summary = plan.daily_summary(day)
                self.assertEqual(summary["kcal"], 150)
                self.assertEqual(summary["protein"], 5)
                self.assertEqual(summary["fat"], 2)
                self.assertEqual(summary["carbs"], 20)

    def test_invalid_day_meal_add_raises(self):
        """Test that adding a meal to an invalid day raises ValueError"""
        invalid_days = ["Funday", "Yesterday", "", None]
        for invalid_day in invalid_days:
            with self.subTest(invalid_day=invalid_day):
                plan = MealPlan()
                with self.assertRaises(ValueError):
                    plan.add_meal(invalid_day, self.basic_recipe)

    def test_multiple_recipes_daily_summary(self):
        """Test correct nutrition summary for multiple recipes in one day"""
        test_cases = [
            (
                "Monday",
                [
                    Recipe("A", {"x": 1}, 100, 10, 5, 5),
                    Recipe("B", {"y": 2}, 200, 20, 10, 10),
                ],
            ),
            ("Tuesday", [Recipe("C", {"z": 3}, 150, 15, 7, 7)]),
            (
                "Wednesday",
                [Recipe("D", {"a": 1}, 80, 8, 4, 3), Recipe("E", {"b": 2}, 120, 10, 5, 5)],
            ),
            ("Thursday", [Recipe("F", {"c": 1}, 300, 25, 12, 15)]),
            ("Friday", [Recipe("G", {"d": 2}, 180, 12, 9, 8)]),
            ("Saturday", [Recipe("H", {"e": 1}, 90, 5, 2, 6)]),
            ("Sunday", [Recipe("I", {"f": 3}, 250, 20, 15, 10)]),
        ]

        for day, recipes in test_cases:
            with self.subTest(day=day):
                plan = MealPlan()
                for r in recipes:
                    plan.add_meal(day, r)

                total_kcal = sum(r.kcal for r in recipes)
                total_protein = sum(r.protein for r in recipes)
                total_fat = sum(r.fat for r in recipes)
                total_carbs = sum(r.carbs for r in recipes)

                summary = plan.daily_summary(day)
                self.assertEqual(summary["kcal"], total_kcal)
                self.assertEqual(summary["protein"], total_protein)
                self.assertEqual(summary["fat"], total_fat)
                self.assertEqual(summary["carbs"], total_carbs)

    def test_mealplan_with_empty_day(self):
        """Test summary for days with no meals"""
        days = ["Monday", "Tuesday", "Wednesday"]
        for day in days:
            with self.subTest(day=day):
                plan = MealPlan()
                plan.plan[day] = []  # Explicitly empty
                self.assertEqual(
                    plan.daily_summary(day),
                    {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
                )

    def test_mealplan_adding_same_recipe_multiple_times(self):
        """Test adding the same recipe multiple times and summing nutritional values"""
        plan = MealPlan()
        r = Recipe("Repeat", {"x": 1}, 100, 5, 5, 5)
        for _ in range(10):
            plan.add_meal("Friday", r)

        summary = plan.daily_summary("Friday")
        self.assertEqual(summary["kcal"], 1000)
        self.assertEqual(summary["protein"], 50)
        self.assertEqual(summary["fat"], 50)
        self.assertEqual(summary["carbs"], 50)

    def test_mealplan_adding_same_meal_to_different_days(self):
        """Test adding the same meal to different days"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            with self.subTest(day=day):
                plan = MealPlan()
                r = Recipe("Multi", {"a": 1}, 100, 10, 1, 1)
                plan.add_meal(day, r)
                self.assertEqual(plan.daily_summary(day)["kcal"], 100)

    def test_mealplan_100_meals_summary_correct(self):
        """Test summing nutritional values for a large number (100) of meals"""
        plan = MealPlan()
        r = Recipe("R", {"z": 1}, 10, 1, 1, 1)
        for _ in range(100):
            plan.add_meal("Monday", r)

        self.assertEqual(plan.daily_summary("Monday")["kcal"], 1000)
        self.assertEqual(plan.daily_summary("Monday")["protein"], 100)
        self.assertEqual(plan.daily_summary("Monday")["fat"], 100)
        self.assertEqual(plan.daily_summary("Monday")["carbs"], 100)

    def test_mealplan_summary_multiple_recipes_varied(self):
        """Test summary correctness for different recipes in one day"""
        plan = MealPlan()
        r1 = Recipe("L1", {"a": 1}, 50, 2, 1, 5)
        r2 = Recipe("L2", {"b": 1}, 100, 3, 1, 10)

        plan.add_meal("Wednesday", r1)
        plan.add_meal("Wednesday", r2)

        summary = plan.daily_summary("Wednesday")
        self.assertEqual(summary["kcal"], 150)
        self.assertEqual(summary["protein"], 5)
        self.assertEqual(summary["fat"], 2)
        self.assertEqual(summary["carbs"], 15)

    def test_mealplan_invalid_recipe_type(self):
        """Test response to adding an invalid recipe type"""
        plan = MealPlan()
        with self.assertRaises(TypeError):
            plan.add_meal("Monday", "not_a_recipe")  # Invalid type

    def test_mealplan_initialization(self):
        """Test correct initialization of an empty meal plan"""
        plan = MealPlan()
        # Check if all days are initialized
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.assertEqual(len(plan.plan), 7)
        for day in days:
            self.assertIn(day, plan.plan)
            self.assertEqual(plan.plan[day], [])

    def test_add_multiple_meals_to_same_day(self):
        """Test adding multiple meals to the same day"""
        mp = MealPlan()
        recipe1 = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
        recipe2 = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)
        recipe3 = Recipe("Dinner", {"chicken": 200}, 300, 30, 10, 0)

        mp.add_meal("Wednesday", recipe1)
        mp.add_meal("Wednesday", recipe2)
        mp.add_meal("Wednesday", recipe3)

        self.assertEqual(len(mp.plan["Wednesday"]), 3)
        self.assertEqual(mp.plan["Wednesday"][0].name, "Breakfast")
        self.assertEqual(mp.plan["Wednesday"][2].name, "Dinner")

        summary = mp.daily_summary("Wednesday")
        self.assertEqual(summary["kcal"], 630)  # 180 + 150 + 300
        self.assertEqual(summary["protein"], 45)  # 12 + 3 + 30
        self.assertEqual(summary["fat"], 21)  # 10 + 1 + 10
        self.assertEqual(summary["carbs"], 35)  # 5 + 30 + 0

    def test_mealplan_invalid_day_summary(self):
        """Test response to getting summary for a non-existent day"""
        plan = MealPlan()
        with self.assertRaises(ValueError):
            plan.daily_summary("NonExistentDay")

    def test_add_same_recipe_multiple_times(self):
        """Test adding the same recipe object multiple times"""
        mp = MealPlan()
        recipe = Recipe("Snack", {"nuts": 50}, 280, 10, 22, 8)

        mp.add_meal("Monday", recipe)
        mp.add_meal("Monday", recipe)  # Same instance added twice

        self.assertEqual(len(mp.plan["Monday"]), 2)
        summary = mp.daily_summary("Monday")
        self.assertEqual(summary["kcal"], 560)  # 280 + 280

    def test_full_week_plan(self):
        """Test creating a full week meal plan"""
        mp = MealPlan()
        breakfast = Recipe("Breakfast", {"eggs": 2}, 180, 12, 10, 5)
        lunch = Recipe("Lunch", {"rice": 100}, 150, 3, 1, 30)
        dinner = Recipe("Dinner", {"chicken": 200}, 300, 30, 10, 0)

        # Add meals for each day
        for day in mp.plan.keys():
            mp.add_meal(day, breakfast)
            mp.add_meal(day, lunch)
            mp.add_meal(day, dinner)

        # Check all days
        for day in mp.plan.keys():
            self.assertEqual(len(mp.plan[day]), 3)

        # Check nutritional values for all days
        summary = mp.daily_summary("Sunday")
        self.assertEqual(summary["kcal"], 630)  # 180 + 150 + 300
        self.assertEqual(summary["protein"], 45)  # 12 + 3 + 30
        self.assertEqual(summary["fat"], 21)  # 10 + 1 + 10
        self.assertEqual(summary["carbs"], 35)  # 5 + 30 + 0


if __name__ == "__main__":
    unittest.main()