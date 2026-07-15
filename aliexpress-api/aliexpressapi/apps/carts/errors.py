class CartConflictError(Exception):
    status_code = 409
    code = "CART_CONFLICT"
