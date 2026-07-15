class CheckoutError(Exception):
    status_code = 400
    code = "CHECKOUT_ERROR"


class EmptyCartError(CheckoutError):
    code = "EMPTY_CART"


class CheckoutConflictError(CheckoutError):
    status_code = 409
    code = "CHECKOUT_CONFLICT"
