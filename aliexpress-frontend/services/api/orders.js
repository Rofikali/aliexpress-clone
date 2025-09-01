// services/api/orders.js
import api from "./index";

export async function getOrders() {
    return api.get("/orders/");
}

export async function getOrderById(id) {
    return api.get(`/orders/${id}/`);
}

export async function placeOrder(orderData) {
    return api.post("/orders/", orderData);
}
