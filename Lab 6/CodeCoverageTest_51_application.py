
import pytest
from self_storage import rent_due, access_allowed, payment_status


# ---------------- RENT DUE TESTS ----------------

def test_invalid_unit_size():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("extra_large", 5, False, False)


def test_negative_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)


def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0


def test_member_small_unit():
    assert rent_due("small", 3, False, True) == 80


def test_member_medium_unit():
    assert rent_due("medium", 4, False, True) == 80


def test_large_unit_member():
    assert rent_due("large", 4, False, True) == 80


def test_climate_control():
    assert rent_due("small", 3, True, False) == 240


def test_non_climate_control():
    assert rent_due("small", 3, False, False) == 160


def test_extra_months_greater_than_six():
    assert rent_due("small", 8, False, False) == 490


def test_climate_extra_months_greater_than_six():
    assert rent_due("small", 8, True, False) == 735


# ---------------- ACCESS ALLOWED TESTS ----------------

def test_owner_access_allowed():
    assert access_allowed(23, 4, True) is True


def test_owner_access_denied():
    assert access_allowed(12, 5, True) is False


def test_visitor_access_before_opening():
    assert access_allowed(5, 1, False) is False


def test_visitor_access_after_closing():
    assert access_allowed(23, 1, False) is False


def test_visitor_access_allowed():
    assert access_allowed(12, 2, False) is True


def test_visitor_limit_exceeded():
    assert access_allowed(12, 3, False) is False


# ---------------- PAYMENT STATUS TESTS ----------------

def test_autopay_current():
    assert payment_status(0, True, False) == "current"


def test_non_autopay_current():
    assert payment_status(5, False, False) == "current"


def test_prior_late_payment():
    assert payment_status(15, False, True) == "current"


def test_grace_period():
    assert payment_status(-1, True, False) == "grace"


def test_lien_status():
    assert payment_status(-16, True, False) == "lien"


def test_grace_period_with_prior_late():
    assert payment_status(0, False, True) == "grace"
