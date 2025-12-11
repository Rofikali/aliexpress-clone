// services/api/wishlist.js
import api from "./index";

export async function getWishlist() {
    return api.get("/wishlist/");
}

export async function addToWishlist(productId) {
    return api.post("/wishlist/", { product_id: productId });
}

export async function removeFromWishlist(productId) {
    return api.delete(`/wishlist/${productId}/`);
}
