// services/api/categories.js
import api from "./index";

export async function getCategories() {
    return api.get("/categories/");
}

export async function getCategoryBySlug(slug) {
    return api.get(`/categories/${slug}/`);
}

export async function getCategoryProducts(slug, params = {}) {
    return api.get(`/categories/${slug}/products/`, { params });
}
