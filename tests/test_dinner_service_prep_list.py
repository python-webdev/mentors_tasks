from tasks.task_01.dinner_service_prep_list import generate_prep_list


def test_generate_prep_list(capsys):
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
    }

    generate_prep_list(par_levels, current_stock)
    captured = capsys.readouterr()
    expected_output = """--- TONIGHT'S KITCHEN PREP LIST ---
onions_kg: NEED 6 kg
tomatoes_kg: OK
chicken_breast_kg: OK
garlic_kg: NEED 1.5 kg
heavy_cream_liters: NEED 5 liters
-----------------------------------
Total items to prep/order: 3
"""
    assert captured.out == expected_output
