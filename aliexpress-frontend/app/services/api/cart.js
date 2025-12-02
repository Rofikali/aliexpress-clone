// services/api/cart.js
import api from "./index";

export async function getCart() {
    return api.get("/cart/");
}

export async function addToCart(productId, quantity = 1) {
    return api.post("/cart/", { product_id: productId, quantity });
}

export async function updateCartItem(itemId, quantity) {
    return api.put(`/cart/${itemId}/`, { quantity });
}

export async function removeFromCart(itemId) {
    return api.delete(`/cart/${itemId}/`);
}
