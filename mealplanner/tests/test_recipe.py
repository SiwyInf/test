### test_recipe.py ###
import pytest
from recipe import Recipe

# Test sprawdzający poprawne utworzenie przepisów z weryfikacją wartości odżywczych
def test_valid_recipe_smoothie():
    r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 180
    assert nutrients["protein"] == 5
    assert nutrients["fat"] == 3
    assert nutrients["carbs"] == 35

def test_valid_recipe_soup():
    r = Recipe("Soup", {"water": 500, "carrot": 100}, 90, 2, 1, 10)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 90
    assert nutrients["protein"] == 2
    assert nutrients["fat"] == 1
    assert nutrients["carbs"] == 10

def test_valid_recipe_rice():
    r = Recipe("Rice", {"rice": 100}, 130, 3, 1, 30)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 130
    assert nutrients["protein"] == 3
    assert nutrients["fat"] == 1
    assert nutrients["carbs"] == 30

def test_valid_recipe_omelette():
    r = Recipe("Omelette", {"eggs": 2, "cheese": 50}, 250, 15, 20, 2)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 250
    assert nutrients["protein"] == 15
    assert nutrients["fat"] == 20
    assert nutrients["carbs"] == 2

def test_valid_recipe_pancakes():
    r = Recipe("Pancakes", {"flour": 100, "milk": 200}, 300, 7, 6, 40)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 300
    assert nutrients["protein"] == 7
    assert nutrients["fat"] == 6
    assert nutrients["carbs"] == 40

# Test sprawdzający, czy podanie pustej nazwy przepisu wywołuje błąd ValueError
def test_invalid_recipe_empty_name():
    with pytest.raises(ValueError):
        Recipe("", {}, 100, 5, 5, 5)
# Test sprawdzający, czy podanie ujemnej wartości kalorii wywołuje błąd ValueError
def test_invalid_recipe_negative_kcal():
    with pytest.raises(ValueError):
        Recipe("Invalid", {}, -10, 5, 5, 5)
# Test sprawdzający, czy podanie ujemnej wartości białka wywołuje błąd ValueError
def test_invalid_recipe_negative_protein():
    with pytest.raises(ValueError):
        Recipe("Invalid", {}, 100, -5, 5, 5)
# Test sprawdzający, czy podanie ujemnej wartości tłuszczu wywołuje błąd ValueError
def test_invalid_recipe_negative_fat():
    with pytest.raises(ValueError):
        Recipe("Invalid", {}, 100, 5, -5, 5)
# Test sprawdzający, czy podanie ujemnej wartości węglowodanów wywołuje błąd ValueError
def test_invalid_recipe_negative_carbs():
    with pytest.raises(ValueError):
        Recipe("Invalid", {}, 100, 5, 5, -5)

# Test dla dużych wartości w przepisach
def test_large_values_recipe():
    r = Recipe("Mega Meal", {"meat": 1000, "rice": 500}, 10000, 500, 200, 600)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 10000
    assert nutrients["protein"] == 500
    assert nutrients["fat"] == 200
    assert nutrients["carbs"] == 600

# Test bardzo dużych wartości
def test_very_large_values_recipe():
    r = Recipe("Ultra Meal", {"meat": 10000, "rice": 5000}, 100000, 5000, 2000, 6000)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 100000
    assert nutrients["protein"] == 5000
    assert nutrients["fat"] == 2000
    assert nutrients["carbs"] == 6000

# Test na ujemną ilość składnika
def test_negative_ingredient_quantity():
    with pytest.raises(ValueError, match="Ingredient quantity for 'milk' cannot be negative"):
        Recipe("Strange", {"milk": -200}, 100, 5, 5, 5)



# Pojedyncze testy na różne długości i formaty nazw (zamiast parametryzacji)
def test_very_long_name():
    name = "A" * 1000  # bardzo długa nazwa
    r = Recipe(name, {"air": 0}, 0, 0, 0, 0)
    assert r.name == name

# Test na składnik o zerowej ilości
def test_zero_ingredient_quantity():
    r = Recipe("ZeroFood", {"water": 0}, 0, 0, 0, 0)
    assert r.ingredients["water"] == 0

# Test na przepis ze wszystkimi wartościami równymi zeru
def test_recipe_with_zero_values_everywhere():
    r = Recipe("ZeroMeal", {}, 0, 0, 0, 0)
    assert r.total_nutrients() == {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}

# Test na przepis z mieszanymi jednostkami
def test_recipe_with_mixed_units():
    r = Recipe("Mixed", {"rice (g)": 100, "milk (ml)": 200}, 350, 15, 10, 40)
    assert "milk (ml)" in r.ingredients

# Test na zachowanie nazwy w przepisie (z użyciem specjalnych znaków)
def test_recipe_str_name_is_preserved():
    name = "Śniadanie #1 -- 🍳🥓"
    r = Recipe(name, {"jajko": 1}, 120, 10, 8, 1)
    assert r.name == name


# Test na przepis z zerową ilością białka
def test_recipe_zero_protein_meal():
    r = Recipe("Woda", {"woda": 200}, 0, 0, 0, 0)
    nutrients = r.total_nutrients()
    assert nutrients["protein"] == 0


# Test sprawdzający obsługę bardzo dużych ilości składników
def test_very_large_quantity():
    r = Recipe("LargeFlour", {"mąka": 99999}, 100, 1, 1, 1)
    assert r.ingredients["mąka"] == 99999

# Test sprawdzający obsługę polskich znaków w nazwie przepisu
def test_polish_chars_name():
    r = Recipe("Śniadanie", {"x": 1}, 100, 1, 1, 1)
    assert r.name == "Śniadanie"
# Test sprawdzający obsługę znaków specjalnych w nazwie przepisu
def test_name_with_special_chars():
    r = Recipe("lunch@12", {"x": 1}, 100, 1, 1, 1)
    assert r.name == "lunch@12"
# Test sprawdzający obsługę podkreślenia w nazwie przepisu
def test_name_with_underscore():
    r = Recipe("kolacja_3", {"x": 1}, 100, 1, 1, 1)
    assert r.name == "kolacja_3"
# Test sprawdzający obsługę emoji w nazwie przepisu
def test_name_with_emoji():
    r = Recipe("🍏🍎🍐🍊", {"x": 1}, 100, 1, 1, 1)
    assert r.name == "🍏🍎🍐🍊"

# Test sprawdzający obsługę kluczy liczbowych zamiast ciągów znaków w słowniku składników
def test_ingredient_keys_are_not_strings():
    r = Recipe("NumericKeys", {1: 100, 2.5: 50}, 100, 1, 1, 1)
    assert r.ingredients[1] == 100
    assert r.ingredients[2.5] == 50

# Test na przekazanie None jako słownik składników
def test_recipe_with_none_ingredient_dict():
    with pytest.raises(TypeError):
        Recipe("NoneIngredients", None, 100, 5, 5, 5)

# Test na reprezentację łańcuchową przepisu
def test_recipe_str_representation():
    r = Recipe("NiceMeal", {"pasta": 200}, 300, 10, 5, 50)
    assert "NiceMeal" in str(r)

# Test sprawdzający obsługę wielu składników w jednym przepisie
def test_recipe_with_multiple_ingredients():
    r = Recipe("ComplexMeal", {"rice": 100, "chicken": 150, "sauce": 50}, 450, 30, 15, 40)
    assert len(r.ingredients) == 3
    assert r.ingredients["rice"] == 100
    assert r.ingredients["chicken"] == 150
    assert r.ingredients["sauce"] == 50

# Test sprawdzający obsługę maksymalnych wartości liczbowych (blisko limitu typu Int)
def test_recipe_with_maximum_values():
    r = Recipe("MaxMeal", {"ingredient": 1}, 2**31-1, 2**31-1, 2**31-1, 2**31-1)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == 2**31-1
    assert nutrients["protein"] == 2**31-1
# Test sprawdzający obsługę wartości dziesiętnych w ilościach składników
def test_recipe_ingredient_with_decimal_value():
    r = Recipe("PreciseRecipe", {"flour": 123.456}, 200, 5, 3, 30)
    assert r.ingredients["flour"] == 123.456
# Test sprawdzający obsługę znaków specjalnych w nazwach składników
def test_recipe_with_special_chars_in_ingredients():
    r = Recipe("SpecialIngredients", {"$pec!al": 100, "normal": 200}, 300, 10, 5, 40)
    assert r.ingredients["$pec!al"] == 100
# Test sprawdzający obsługę znaków Unicode w nazwach składników
def test_recipe_with_unicode_ingredient_names():
    r = Recipe("UnicodeIngredients", {"śliwki": 10, "jabłka": 5}, 150, 2, 1, 30)
    assert r.ingredients["śliwki"] == 10
    assert r.ingredients["jabłka"] == 5
# Test sprawdzający spójność wartości odżywczych między metodą total_nutrients() a atrybutami klasy
def test_recipe_nutritional_values_consistency():
    r = Recipe("TestConsistency", {"test": 100}, 200, 10, 5, 25)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == r.kcal
    assert nutrients["protein"] == r.protein
    assert nutrients["fat"] == r.fat
    assert nutrients["carbs"] == r.carbs
# Test sprawdzający obsługę ilości składnika równej 1
def test_recipe_with_ingredient_quantity_one():
    r = Recipe("SingleUnit", {"egg": 1}, 80, 6, 5, 0)
    assert r.ingredients["egg"] == 1
# Test sprawdzający maksymalną długość nazwy przepisu
def test_recipe_max_name_length():
    long_name = "X" * 10000  # Bardzo długa nazwa
    r = Recipe(long_name, {"x": 1}, 100, 5, 5, 5)
    assert r.name == long_name
# Test sprawdzający obsługę wartości logicznych jako kluczy w słowniku składników
def test_recipe_with_boolean_ingredient_keys():
    r = Recipe("BoolKeys", {True: 100, False: 50}, 150, 5, 5, 5)
    assert r.ingredients[True] == 100
    assert r.ingredients[False] == 50

# Test sprawdzający obsługę krotek jako kluczy w słowniku składników
def test_recipe_with_tuple_ingredient_keys():
    r = Recipe("TupleKeys", {("apple", "fresh"): 3, ("banana", "ripe"): 2}, 200, 5, 2, 30)
    assert r.ingredients[("apple", "fresh")] == 3
    assert r.ingredients[("banana", "ripe")] == 2





