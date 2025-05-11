
# 🥗 Aplikacja Planowania Posiłków

Prosta aplikacja oparta na Pythonie do zarządzania planami posiłków, przepisami i listami zakupów. Skupia się na przejrzystym śledzeniu wartości odżywczych i skutecznym zarządzaniu zakupami spożywczymi.

---

## 🚀 Główne Funkcje

- ✅ Zarządzanie codziennymi planami posiłków  
- ✅ Tworzenie i walidacja przepisów z wartościami odżywczymi  
- ✅ Automatyczne generowanie list zakupów  
- ✅ Filtrowanie i kategoryzacja produktów spożywczych  
- ✅ Pokrycie testami na poziomie 99% dzięki `pytest` i `coverage.py`

---

## 🧪 Technologie Wykorzystane

- **Python 3.x**  
- **Pytest** — testy jednostkowe  
- **Coverage.py** — analiza pokrycia kodu testami

---

## 🗂️ Struktura Projektu

```
mealplanner/
├── src/
│   ├── recipe.py
│   ├── mealplan.py
│   └── shoppinglist.py
├── tests/
│   ├── test_recipe.py
│   ├── test_mealplan.py
│   └── test_shoppinglist.py
├── requirements.txt
└── README.md
```

---

## 📦 Instalacja

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/SiwyInf/PF169366
   cd mealplanner
   ```

2. **Zainstaluj wymagane biblioteki:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Zainstaluj narzędzie do analizy pokrycia kodu:**
   ```bash
   pip install coverage
   ```

---

## ❓ Wyjaśnienie Poleceń

- `pip install coverage`  
  ➤ Instaluje bibliotekę `coverage`, służącą do mierzenia, jak duża część kodu jest objęta testami jednostkowymi.

- `pip install -r requirements.txt`  
  ➤ Instaluje wszystkie wymagane biblioteki wymienione w pliku `requirements.txt`, niezbędne do uruchomienia aplikacji.

---

## 🧪 Uruchamianie Testów

- **Uruchomienie wszystkich testów:**
  ```bash
  pytest
  ```

- **Uruchomienie testów z raportem pokrycia:**
  ```bash
  coverage run -m pytest -s tests
  coverage report
  ```

---

---

## 📚 Źródła i Wsparcie

W trakcie pracy nad aplikacją korzystano z dodatkowych źródeł wspierających proces nauki i zrozumienia narzędzi:

- **Claude AI** – pomoc w głębszym zrozumieniu zasad działania testów jednostkowych oraz interpretacji ich wyników.
- **ChatGPT (OpenAI)** – wsparcie w analizie struktury aplikacji, dokumentacji oraz ogólnym zrozumieniu działania poszczególnych komponentów.
- **Oficjalna dokumentacja Pytest** – [https://docs.pytest.org/en/stable/contents.html](https://docs.pytest.org/en/stable/contents.html) – źródło wiedzy przy konfiguracji i użyciu `pytest` do testowania aplikacji.


## 👨‍💻 Autorzy

- **Marcel Szeluga** – [GitHub](https://github.com/SiwyInf)

---

