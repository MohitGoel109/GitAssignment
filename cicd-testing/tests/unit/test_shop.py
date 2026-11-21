import pytest

from app.shop import calculate_total, is_valid_email


def test_total_without_discount():
    items = [{"price": 10.0, "qty": 3}, {"price": 5.5, "qty": 2}]
    assert calculate_total(items) == 41.0


def test_total_with_discount():
    assert calculate_total([{"price": 100, "qty": 1}], 25) == 75.0


def test_total_of_empty_cart_is_zero():
    assert calculate_total([]) == 0


def test_invalid_discount_raises_error():
    with pytest.raises(ValueError):
        calculate_total([{"price": 10, "qty": 1}], 150)


def test_valid_email_is_accepted():
    assert is_valid_email("user@example.com") is True


@pytest.mark.parametrize("email", ["no-at-sign", "a@b", "@x.com", None])
def test_invalid_email_is_rejected(email):
    assert is_valid_email(email) is False
