// services/api/products.js
import api from "./index";

export async function getProducts(params = {}) {
    return api.get("/products/", { params });
}

export async function getProductById(id) {
    return api.get(`/products/${id}/`);
}

export async function searchProducts(query, params = {}) {
    return api.get("/products/search/", { params: { q: query, ...params } });
}

// For sellers/admin
export async function createProduct(productData) {
    return api.post("/products/", productData);
}

export async function updateProduct(id, productData) {
    return api.put(`/products/${id}/`, productData);
}

export async function deleteProduct(id) {
    return api.delete(`/products/${id}/`);
}
