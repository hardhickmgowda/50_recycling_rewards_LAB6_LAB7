"""Lab 6 - Step 7: test cases written to reach >= 90% BRANCH coverage.

Every `if` is driven both True and False, including boundary values.

Run:
    coverage run --branch -m pytest BranchCoverageTest_recycling_rewards.py
    coverage report -m
"""
import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------------- reward_points ----------------
def test_unknown_material():                       # line 5 True
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_negative_weight():                        # line 7 True
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


def test_zero_weight_is_valid():                   # line 7 False, line 13 True
    assert reward_points("paper", 0, False) == 0


def test_exactly_minimum_gives_zero():             # boundary: extra == 0
    assert reward_points("paper", 5, False) == 0


def test_below_minimum_weight():                   # line 13 True
    assert reward_points("paper", 3, False) == 0


def test_bonus_applies_to_paper():                 # line 10 True
    assert reward_points("paper", 10, True) == 36  # min 4, extra 6, rate 6


def test_bonus_applies_to_plastic():               # line 10 True
    assert reward_points("plastic", 3, True) == 6  # min 2, extra 1, rate 6


def test_bonus_ignored_for_metal():                # line 10 False (has_bonus, metal)
    assert reward_points("metal", 10, True) == 96  # min 2, extra 8, rate 12


def test_no_bonus_paper():                         # line 10 False (no bonus)
    assert reward_points("paper", 10, False) == 30


def test_metal_normal_rate():                      # line 15 True, line 19 False
    assert reward_points("metal", 10, False) == 96


def test_non_metal_rate():                         # line 15 False
    assert reward_points("plastic", 10, False) == 42  # extra 7 * 6


def test_extra_exactly_20_not_high_volume():       # boundary: extra == 20 -> line 19 False
    assert reward_points("paper", 25, False) == 120   # 20 * 6
    assert reward_points("metal", 22, False) == 240   # 20 * 12


def test_extra_21_paper_high_volume():             # line 19 True, line 21 False
    assert reward_points("paper", 26, False) == 210   # 21 * (6 + 4)


def test_extra_21_metal_high_volume():             # line 19 True, line 21 True
    assert reward_points("metal", 23, False) == 378   # 21 * (12 + 4 + 2)


# ---------------- collection_accepted ----------------
def test_hazardous_at_limit():                     # line 27 True
    assert collection_accepted(5, 1, True) is True


def test_hazardous_over_limit():
    assert collection_accepted(5.1, 1, True) is False


def test_non_hazardous_too_heavy():                # line 29 True
    assert collection_accepted(50.1, 1, False) is False


def test_non_hazardous_at_weight_limit():          # line 29 False
    assert collection_accepted(50, 3, False) is True


def test_non_hazardous_too_many_bags():
    assert collection_accepted(20, 4, False) is False


# ---------------- slot_status ----------------
def test_morning_open_at_cutoff():                 # line 35 True, line 41 True
    assert slot_status(20, True, False) == "open"


def test_morning_late_just_below_cutoff():         # line 41 False, line 43 True
    assert slot_status(19, True, False) == "late"


def test_morning_late_lower_edge():
    assert slot_status(5, True, False) == "late"


def test_morning_missed():                         # line 43 False
    assert slot_status(4, True, False) == "missed"


def test_evening_open_at_cutoff():                 # line 35 False
    assert slot_status(10, False, False) == "open"


def test_evening_late():
    assert slot_status(9, False, False) == "late"


def test_evening_missed():
    assert slot_status(-6, False, False) == "missed"


def test_holiday_open_at_cutoff():                 # line 39 True
    assert slot_status(35, True, True) == "open"


def test_holiday_late():
    assert slot_status(34, True, True) == "late"


def test_holiday_evening_open():
    assert slot_status(25, False, True) == "open"


def test_non_holiday_cutoff_not_extended():       # line 39 False
    assert slot_status(25, True, False) == "open"
