import pytest
from src.recipe import Recipe


################################################################
# 1. TESTY PODSTAWOWEJ INICJALIZACJI PRZEPISU                  #
################################################################

@pytest.mark.parametrize(
    "name,ingredients,kcal,protein,fat,carbs",
    [
        ("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35),
        ("Soup", {"water": 500, "carrot": 100}, 90, 2, 1, 10),
        ("Rice", {"rice": 100}, 130, 3, 1, 30),
        ("Omelette", {"eggs": 2, "cheese": 50}, 250, 15, 20, 2),
        ("Pancakes", {"flour": 100, "milk": 200}, 300, 7, 6, 40),
    ],
)
def test_valid_recipe_creation(name, ingredients, kcal, protein, fat, carbs):
    """Testy sprawdzające poprawne tworzenie przepisów"""
    r = Recipe(name, ingredients, kcal, protein, fat, carbs)
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == kcal
    assert nutrients["protein"] == protein
    assert nutrients["fat"] == fat
    assert nutrients["carbs"] == carbs


################################################################
# 2. TESTY WALIDACJI DANYCH WEJŚCIOWYCH                        #
################################################################

def test_invalid_recipe_empty_name():
    """Test sprawdzający reakcję na pustą nazwę przepisu"""
    with pytest.raises(ValueError):
        Recipe("", {}, 100, 5, 5, 5)

@pytest.mark.parametrize(
    "kcal,protein,fat,carbs",
    [(-10, 5, 5, 5), (100, -5, 5, 5), (100, 5, -5, 5), (100, 5, 5, -5)],
)
def test_invalid_nutritional_values(kcal, protein, fat, carbs):
    """Testy sprawdzające reakcję na ujemne wartości odżywcze"""
    with pytest.raises(ValueError):
        Recipe("Invalid", {}, kcal, protein, fat, carbs)

def test_negative_ingredient_quantity():
    """Test sprawdzający reakcję na ujemną ilość składnika"""
    with pytest.raises(ValueError, match="Ingredient quantity for 'milk' cannot be negative"):
        Recipe("Strange", {"milk": -200}, 100, 5, 5, 5)

def test_recipe_with_none_ingredient_dict():
    """Test sprawdzający reakcję na None jako słownik składników"""
    with pytest.raises(TypeError):
        Recipe("NoneIngredients", None, 100, 5, 5, 5)


################################################################
# 3. TESTY SPECJALNYCH PRZYPADKÓW I WARTOŚCI BRZEGOWYCH        #
################################################################

@pytest.mark.parametrize(
    "name,ingredients,kcal,protein,fat,carbs",
    [
        ("ZeroMeal", {}, 0, 0, 0, 0),
        ("ZeroFood", {"water": 0}, 0, 0, 0, 0),
        ("SingleUnit", {"egg": 1}, 80, 6, 5, 0),
        ("PreciseRecipe", {"flour": 123.456}, 200, 5, 3, 30),
    ],
)
def test_edge_case_recipes(name, ingredients, kcal, protein, fat, carbs):
    """Testy sprawdzające specjalne przypadki wartości"""
    r = Recipe(name, ingredients, kcal, protein, fat, carbs)
    assert r.total_nutrients() == {
        "kcal": kcal,
        "protein": protein,
        "fat": fat,
        "carbs": carbs,
    }

@pytest.mark.parametrize(
    "quantity,expected", [(99999, 99999), (2**31 - 1, 2**31 - 1), (123.456, 123.456)]
)
def test_large_and_special_quantities(quantity, expected):
    """Testy sprawdzające duże i specjalne wartości ilości składników"""
    r = Recipe("QtyTest", {"ingredient": quantity}, 100, 1, 1, 1)
    assert r.ingredients["ingredient"] == expected

@pytest.mark.parametrize("quantity", [0, 1e6, 1.5, -1])
def test_recipe_with_extreme_quantities(quantity):
    """Testuje reakcję na skrajne wartości ilości składników."""
    if quantity < 0:
        with pytest.raises(ValueError):
            Recipe("Test", {"ingredient": quantity}, 100, 1, 1, 1)
    else:
        r = Recipe("Test", {"ingredient": quantity}, 100, 1, 1, 1)
        assert r.ingredients["ingredient"] == quantity


################################################################
# 4. TESTY NAZW PRZEPISÓW I SKŁADNIKÓW                        #
################################################################

@pytest.mark.parametrize(
    "name",
    [
        "Śniadanie #1 -- 🍳🥓",
        "lunch@12",
        "kolacja_3",
        "🍏🍎🍐🍊",
        "X" * 10000,
        "Śniadanie",
    ],
)
def test_special_recipe_names(name):
    """Testy sprawdzające specjalne formaty nazw przepisów"""
    r = Recipe(name, {"x": 1}, 100, 1, 1, 1)
    assert r.name == name

@pytest.mark.parametrize(
    "ingredients",
    [
        {"$pec!al": 100, "normal": 200},
        {"śliwki": 10, "jabłka": 5},
        {1: 100, 2.5: 50},
        {True: 100, False: 50},
        {("apple", "fresh"): 3, ("banana", "ripe"): 2},
    ],
)
def test_special_ingredient_names(ingredients):
    """Testy sprawdzające specjalne formaty nazw składników"""
    r = Recipe("SpecialIngredients", ingredients, 300, 10, 5, 40)
    for ing, qty in ingredients.items():
        assert r.ingredients[ing] == qty


################################################################
# 5. TESTY METOD OPERUJĄCYCH NA SKŁADNIKACH                   #
################################################################

def test_ingredient_operations():
    """Testy sprawdzające operacje na składnikach"""
    r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)

    # Test add_ingredient
    r.add_ingredient("strawberry", 50)
    assert "strawberry" in r.ingredients
    assert r.ingredients["strawberry"] == 50

    # Test contains_ingredient
    assert r.contains_ingredient("banana") == True
    assert r.contains_ingredient("apple") == False

    # Test update_ingredient_quantity
    r.update_ingredient_quantity("banana", 2)
    assert r.ingredients["banana"] == 2

    # Test remove_ingredient
    r.remove_ingredient("banana")
    assert "banana" not in r.ingredients

    # Test total_weight
    assert r.total_weight() == 250  # 200 (milk) + 50 (strawberry)

@pytest.mark.parametrize(
    "method,args,error",
    [
        ("add_ingredient", ("strawberry", -50), ValueError),
        ("update_ingredient_quantity", ("milk", -1), ValueError),
        ("remove_ingredient", ("nonexistent",), None),  # Should not raise
    ],
)
def test_ingredient_operations_edge_cases(method, args, error):
    """Testy sprawdzające edge case'y operacji na składnikach"""
    r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)
    func = getattr(r, method)

    if error:
        with pytest.raises(error):
            func(*args)
    else:
        func(*args)  # Should not raise


################################################################
# 6. TESTY OPERACJI NA WARTOŚCIACH ODŻYWCZYCH                 #
################################################################

def test_nutrition_updates():
    """Testy sprawdzające aktualizację wartości odżywczych"""
    r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)

    r.update_kcal(200)
    assert r.kcal == 200

    r.update_protein(7)
    assert r.protein == 7

    r.update_fat(4)
    assert r.fat == 4

    r.update_carbs(40)
    assert r.carbs == 40

    # Test consistency
    nutrients = r.total_nutrients()
    assert nutrients["kcal"] == r.kcal
    assert nutrients["protein"] == r.protein
    assert nutrients["fat"] == r.fat
    assert nutrients["carbs"] == r.carbs


################################################################
# 7. TESTY OPERACJI NA CAŁYM PRZEPISIE                        #
################################################################

def test_recipe_scaling():
    """Testy sprawdzające skalowanie przepisu"""
    r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)

    # Test normal scaling
    r.scale_recipe(2)
    assert r.ingredients["banana"] == 2
    assert r.ingredients["milk"] == 400
    assert r.kcal == 360
    assert r.protein == 10

    # Test invalid scaling
    with pytest.raises(ValueError):
        r.scale_recipe(0)

def test_recipe_splitting():
    """Testy sprawdzające dzielenie przepisu na porcje"""
    r = Recipe("Smoothie", {"banana": 1, "milk": 200}, 180, 5, 3, 35)

    r_split = r.split_into_portions(2)
    assert r_split.name == "Smoothie (1/2 portion)"
    assert r_split.kcal == 90
    assert r_split.ingredients["banana"] == 0.5

    with pytest.raises(ValueError):
        r.split_into_portions(0)

def test_recipe_scale_with_invalid_values():
    """Test skalowania przepisu z nieprawidłowymi wartościami"""
    r = Recipe("Test", {"a": 1}, 100, 1, 1, 1)

    with pytest.raises(ValueError):
        r.scale_recipe(-1)

    with pytest.raises(ValueError):
        r.scale_recipe(0)


################################################################
# 8. TESTY PORÓWNYWANIA PRZEPISÓW                             #
################################################################

@pytest.mark.parametrize(
    "r1,r2,expected",
    [
        (
            Recipe("Same", {"a": 1}, 100, 5, 5, 5),
            Recipe("Same", {"a": 1}, 100, 5, 5, 5),
            True,
        ),
        (
            Recipe("DiffName", {"a": 1}, 100, 5, 5, 5),
            Recipe("Other", {"a": 1}, 100, 5, 5, 5),
            False,
        ),
        (
            Recipe("Same", {"a": 1}, 100, 5, 5, 5),
            Recipe("Same", {"a": 2}, 100, 5, 5, 5),
            False,
        ),
        (
            Recipe("Same", {"a": 1}, 100, 5, 5, 5),
            Recipe("Same", {"a": 1}, 200, 5, 5, 5),
            False,
        ),
    ],
)
def test_recipe_equality(r1, r2, expected):
    """Testy sprawdzające porównywanie przepisów"""
    assert (r1 == r2) == expected


################################################################
# 9. TESTY REPREZENTACJI TEKSTOWYCH                           #
################################################################

def test_string_representations():
    """Testy sprawdzające reprezentacje tekstowe przepisu"""
    r = Recipe("NiceMeal", {"pasta": 200, "sauce": 50}, 300, 10, 5, 50)

    # Test basic str
    assert "NiceMeal" in str(r)
    assert "pasta: 200" in str(r)

    # Test detailed str
    detailed = r.detailed_str()
    assert "Recipe: NiceMeal" in detailed
    assert "- pasta: 200g" in detailed
    assert "- kcal: 300" in detailed
    assert "- protein: 10g" in detailed