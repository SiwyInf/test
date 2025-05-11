from typing import Dict  # Import typu słownikowego (klucz: wartość) dla lepszej czytelności i podpowiedzi typów


# Definicja klasy Recipe (Przepis)
class Recipe:
    # Konstruktor klasy, przyjmuje nazwę przepisu, składniki (ze wskazaniem ilości), oraz wartości odżywcze
    def __init__(self, name: str, ingredients: Dict[str, float], kcal: int, protein: int, fat: int, carbs: int):
        # Sprawdzenie, czy nazwa nie jest pusta oraz czy wartości odżywcze nie są ujemne
        if not name or kcal < 0 or protein < 0 or fat < 0 or carbs < 0:
            raise ValueError("Invalid nutritional values or name")  # Rzuca wyjątek, jeśli dane są niepoprawne

        # Sprawdzenie, czy składniki nie są None
        if ingredients is None:
            raise TypeError("Ingredients cannot be None")  # Rzuca wyjątek, jeśli składniki nie zostały podane

        # Sprawdzenie, czy każda ilość składnika nie jest ujemna
        for ingredient, quantity in ingredients.items():
            if quantity < 0:
                raise ValueError(f"Ingredient quantity for '{ingredient}' cannot be negative")  # Błąd, jeśli ilość < 0

        # Przypisanie wartości do pól obiektu
        self.name = name
        self.ingredients = ingredients
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs

    # Metoda zwracająca słownik z łącznymi wartościami odżywczymi przepisu
    def total_nutrients(self) -> Dict[str, int]:
        return {
            "kcal": self.kcal,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs
        }

    # Metoda zamieniająca obiekt na czytelny tekst (np. do printowania)
    def __str__(self):
        return f"Recipe(name={self.name}, kcal={self.kcal}, protein={self.protein}, fat={self.fat}, carbs={self.carbs})"
