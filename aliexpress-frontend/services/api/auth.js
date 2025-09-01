// services/api/auth.js
import api from "./index";

export async function login(email, password) {
    return api.post("/auth/login/", { email, password });
}

export async function register(userData) {
    return api.post("/register/", userData);
}

export async function refreshToken(refresh) {
    return api.post("/auth/refresh/", { refresh });
}

export async function logout() {
    return api.post("/auth/logout/");
}

export async function getProfile() {
    return api.get("/profile/");
}
