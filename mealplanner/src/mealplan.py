from typing import Dict, List
from recipe import Recipe  # Import klasy Recipe z innego modułu


class MealPlan:
    def __init__(self):
        # Inicjalizacja pustego planu posiłków na każdy dzień tygodnia
        # Klucze to dni tygodnia, a wartości to listy obiektów typu Recipe (przepis)
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

    def add_meal(self, day: str, meal: Recipe):
        # Sprawdzenie, czy przekazany posiłek jest instancją klasy Recipe
        if not isinstance(meal, Recipe):
            raise TypeError("meal must be an instance of Recipe")

        # Sprawdzenie, czy podany dzień istnieje w planie
        if day not in self.plan:
            raise ValueError("Invalid day")

        # Dodanie posiłku (obiektu Recipe) do listy posiłków danego dnia
        self.plan[day].append(meal)

    def daily_summary(self, day: str) -> Dict[str, int]:
        # Zwraca podsumowanie wartości odżywczych (kalorie, białko, tłuszcze, węglowodany) dla danego dnia
        if day not in self.plan:
            raise ValueError("Invalid day")

        # Inicjalizacja słownika na sumy wartości odżywczych
        total = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

        # Iteracja po wszystkich przepisach zaplanowanych na dany dzień
        for recipe in self.plan[day]:
            # Pobranie wartości odżywczych z danego przepisu
            nutrients = recipe.total_nutrients()

            # Sumowanie wartości odżywczych
            for key in total:
                total[key] += nutrients[key]

        # Zwrócenie podsumowania
        return total
