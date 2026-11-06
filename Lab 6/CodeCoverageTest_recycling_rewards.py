"""Lab 6 - Step 5: test cases written to reach >= 90% LINE coverage.

Run:
    coverage run -m pytest CodeCoverageTest_recycling_rewards.py
    coverage report -m
"""
import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------------- reward_points ----------------
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0


def test_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)


def test_paper_with_bonus():
    # minimum 5 - 1 = 4, extra = 6, rate = 6
    assert reward_points("paper", 10, True) == 36


def test_paper_no_bonus():
    # minimum 5, extra = 5, rate = 6
    assert reward_points("paper", 10, False) == 30


def test_metal_normal_rate():
    # minimum 2, extra = 8, rate = 12
    assert reward_points("metal", 10, False) == 96


def test_metal_high_volume():
    # minimum 2, extra = 28 (> 20), rate = 12 + 4 + 2 = 18
    assert reward_points("metal", 30, False) == 504


def test_paper_high_volume():
    # minimum 5, extra = 25 (> 20), rate = 6 + 4 = 10
    assert reward_points("paper", 30, False) == 250


# ---------------- collection_accepted ----------------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_collection():
    assert collection_accepted(4, 1, True) is True


def test_too_heavy_collection():
    assert collection_accepted(60, 1, False) is False


# ---------------- slot_status ----------------
def test_slot_open_morning():
    assert slot_status(25, True, False) == "open"


def test_slot_late_evening():
    assert slot_status(5, False, False) == "late"


def test_slot_missed_morning():
    assert slot_status(0, True, False) == "missed"


def test_slot_holiday_extends_cutoff():
    assert slot_status(35, True, True) == "open"
