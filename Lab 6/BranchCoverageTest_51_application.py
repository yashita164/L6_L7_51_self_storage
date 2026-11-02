
import pytest
from self_storage import rent_due, access_allowed, payment_status


# ==========================================
# RENT DUE - BRANCH COVERAGE TESTS
# ==========================================

def test_invalid_unit_size():
    with pytest.raises(ValueError):
        rent_due("invalid", 2, False, False)


def test_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


def test_member_small_unit():
    assert rent_due("small", 3, False, True) == 80


def test_member_medium_unit():
    assert rent_due("medium", 4, False, True) == 80


def test_member_large_unit():
    assert rent_due("large", 4, False, True) == 80


def test_non_member():
    assert rent_due("small", 3, False, False) == 160


def test_no_extra_months():
    assert rent_due("small", 1, False, False) == 0


def test_climate_control():
    assert rent_due("small", 3, True, False) == 240


def test_non_climate_control():
    assert rent_due("small", 3, False, False) == 160


def test_extra_months_not_greater_than_six():
    assert rent_due("small", 7, False, False) == 480


def test_extra_months_greater_than_six():
    assert rent_due("small", 8, False, False) == 490


def test_climate_extra_months_greater_than_six():
    assert rent_due("small", 8, True, False) == 735


# ==========================================
# ACCESS ALLOWED - BRANCH COVERAGE TESTS
# ==========================================

def test_owner_within_visitor_limit():
    assert access_allowed(23, 4, True) is True


def test_owner_exceeds_visitor_limit():
    assert access_allowed(12, 5, True) is False


def test_non_owner_before_opening():
    assert access_allowed(5, 1, False) is False


def test_non_owner_after_closing():
    assert access_allowed(23, 1, False) is False


def test_non_owner_within_allowed_hours():
    assert access_allowed(12, 2, False) is True


def test_non_owner_exceeds_visitor_limit():
    assert access_allowed(12, 3, False) is False


# ==========================================
# PAYMENT STATUS - BRANCH COVERAGE TESTS
# ==========================================

def test_autopay_current():
    assert payment_status(0, True, False) == "current"


def test_non_autopay_current():
    assert payment_status(5, False, False) == "current"


def test_prior_late_payment_current():
    assert payment_status(15, False, True) == "current"


def test_grace_period():
    assert payment_status(-1, True, False) == "grace"


def test_lien_status():
    assert payment_status(-16, True, False) == "lien"


def test_grace_period_with_prior_late():
    assert payment_status(0, False, True) == "grace"
