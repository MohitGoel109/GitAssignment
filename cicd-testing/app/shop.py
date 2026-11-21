def calculate_total(items, discount_percent=0):
    """Return the order total after applying a percentage discount."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount must be between 0 and 100")
    subtotal = sum(item["price"] * item["qty"] for item in items)
    return round(subtotal * (1 - discount_percent / 100), 2)


def is_valid_email(email):
    if not isinstance(email, str) or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain
