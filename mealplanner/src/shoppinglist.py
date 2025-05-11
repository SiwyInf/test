from collections import defaultdict
from recipe import Recipe
from mealplan import MealPlan


# Funkcja do generowania shopping listy
def generate_shopping_list(recipes):
    shopping_list = defaultdict(float)
    for recipe in recipes:
        for ingredient, quantity in recipe.ingredients.items():
            shopping_list[ingredient] += quantity
    return dict(shopping_list)


class ShoppingList:
    def __init__(self):
        self.items = defaultdict(float)

    def add_item(self, ingredient: str, quantity: float):
        # Dodaje składnik i jego ilość do listy zakupów
        if quantity > 0:
            self.items[ingredient] += quantity

    def get_items(self):
        # Zwraca wszystkie składniki na liście zakupów w formie słownika
        return dict(self.items)

    def add_from_recipe(self, recipe: Recipe):
        # Dodaje składniki z pojedynczego przepisu do listy zakupów
        for ingredient, quantity in recipe.ingredients.items():
            self.add_item(ingredient, quantity)

    def add_from_mealplan(self, meal_plan: MealPlan):
        # Dodaje składniki ze wszystkich przepisów w planie posiłków
        for meals in meal_plan.plan.values():
            for recipe in meals:
                self.add_from_recipe(recipe)

    def filter_by_threshold(self, threshold: float):
        # Zwraca filtrowaną listę zakupów z pozycjami, których ilość przekracza próg
        filtered = ShoppingList()
        for ingredient, quantity in self.items.items():
            if quantity >= threshold:
                filtered.add_item(ingredient, quantity)
        return filtered

    def remove_item(self, ingredient: str):
        # Usuwa składnik z listy zakupów
        if ingredient in self.items:
            del self.items[ingredient]

    def clear(self):
        # Czyści listę zakupów
        self.items.clear()

    def update_item_quantity(self, ingredient: str, quantity: float):
        # Aktualizuje ilość składnika w liście zakupów
        if ingredient in self.items:
            if quantity > 0:
                self.items[ingredient] = quantity

    def get_total_items(self):
        # Zwraca całkowitą liczbę unikalnych składników na liście zakupów
        return len(self.items)

    def get_total_quantity(self):
        # Zwraca całkowitą ilość wszystkich składników na liście zakupów
        return sum(self.items.values())

    def get_categorized_items(self):
        # Zwraca składniki pogrupowane według ich domyślnej kategorii
        categories = defaultdict(dict)
        for ingredient, quantity in self.items.items():
            category = "uncategorized"  # Można to rozbudować, aby obsługiwało rzeczywiste kategorie
            categories[category][ingredient] = quantity
        return categories

    def has_item(self, ingredient: str):
        # Sprawdza, czy lista zakupów zawiera dany składnik
        return ingredient in self.items

    def get_item_quantity(self, ingredient: str):
        # Zwraca ilość danego składnika na liście zakupów
        return self.items.get(ingredient, 0)

    def export(self):
        # Eksportuje listę zakupów do słownika
        return dict(self.items)

    def import_list(self, data):
        # Importuje listę zakupów z danych (słownika)
        self.items = defaultdict(float, data)

    def merge(self, other):
        # Łączy inną listę zakupów z bieżącą
        merged = ShoppingList()
        merged.items.update(self.items)  # Kopiuje obecne składniki
        for ingredient, quantity in other.items.items():
            merged.add_item(ingredient, quantity)  # Dodaje składniki z innej listy
        return merged

    def scale_quantities(self, factor: float):
        # Skaluje ilości wszystkich składników przez podany współczynnik
        if factor < 0:
            raise ValueError("Scale factor must be non-negative.")  # WALIDACJA
        for ingredient in self.items:
            self.items[ingredient] *= factor
