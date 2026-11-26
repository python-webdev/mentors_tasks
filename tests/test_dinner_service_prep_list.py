import pytest

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


@pytest.mark.parametrize(
    ("par", "stock", "expected_line"),
    [
        ({"garlic_kg": 1}, {"garlic_kg": 0.9}, "garlic_kg: NEED 0.1 kg"),
        ({"onions_kg": 10.0}, {"onions_kg": 4.0}, "onions_kg: NEED 6 kg"),
        ({"saffron_kg": 0.005}, {"saffron_kg": 0.001}, "saffron_kg: NEED 0.004 kg"),
        ({"milk_liters": 3}, {}, "milk_liters: NEED 3 liters"),
        ({"eggs": 12}, {"eggs": 5}, "eggs: NEED 7 units"),
        ({"eggs": 12}, {"eggs": 12}, "eggs: OK"),
    ],
)
def test_prep_list_line_formatting(capsys, par, stock, expected_line):
    generate_prep_list(par, stock)
    lines = capsys.readouterr().out.splitlines()
    assert lines[1] == expected_line
