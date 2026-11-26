"""
Homework: Dinner Service Prep-List Generator

Scenario:
Before every dinner service, a kitchen checks its current stock against
the par levels (the minimum stock required for the shift). Write a Python
script that compares what is currently in the walk-in cooler against
tonight's par levels and prints a clean Prep & Order Sheet for the team.

Tasks:
1. Loop through every ingredient in `par_levels`.
2. Compare the required `par_levels` amount with what is in `current_stock`:
   - If `current_stock` is less than the par level, calculate how much is
     missing and print: "<ingredient>: NEED <amount> <unit>"
   - If `current_stock` is greater than or equal to the par level, print:
     "<ingredient>: OK"
3. At the bottom, print the total number of items that need attention.

Expected Output:
--- TONIGHT'S KITCHEN PREP LIST ---
onions_kg: NEED 6 kg
tomatoes_kg: OK
chicken_breast_kg: OK
garlic_kg: NEED 1.5 kg
heavy_cream_liters: NEED 5 liters
-----------------------------------
Total items to prep/order: 3

Bonus Challenge:
- Remove "heavy_cream_liters": 0 from `current_stock` and handle missing
  items safely without raising a KeyError.
- Wrap your logic inside a reusable function: generate_prep_list(par, stock)
"""

from collections.abc import Mapping


def _unit_for(ingredient: str) -> str:
    if ingredient.endswith("_liters"):
        return "liters"
    if ingredient.endswith("_kg"):
        return "kg"
    return "units"


def generate_prep_list(
    par: Mapping[str, float], stock: Mapping[str, float]
) -> None:
    print("--- TONIGHT'S KITCHEN PREP LIST ---")
    needs_attention = 0
    for ingredient, required in par.items():
        available = stock.get(ingredient, 0)
        unit = _unit_for(ingredient)
        if available < required:
            missing_amount = required - available
            print(f"{ingredient}: NEED {missing_amount} {unit}")
            needs_attention += 1
        else:
            print(f"{ingredient}: OK")
    print("-----------------------------------")
    print(f"Total items to prep/order: {needs_attention}")


if __name__ == "__main__":
    par_levels = {
        "onions_kg": 10,
        "tomatoes_kg": 8,
        "chicken_breast_kg": 15,
        "garlic_kg": 2,
        "heavy_cream_liters": 5,
    }

    current_stock = {
        "onions_kg": 4,
        "tomatoes_kg": 8,
        "chicken_breast_kg": 18,
        "garlic_kg": 0.5,
        # heavy_cream_liters is intentionally omitted to demonstrate safe handling.
    }

    generate_prep_list(par_levels, current_stock)
