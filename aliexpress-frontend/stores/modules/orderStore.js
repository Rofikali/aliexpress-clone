// stores/modules/orderStore.js
import { defineStore } from "pinia";
import { getOrders, getOrderById, placeOrder } from "~/services/api/orders";

export const useOrderStore = defineStore("orders", () => {
    const orders = ref([]);
    const currentOrder = ref(null);
    const loading = ref(false);
    const error = ref(null);

    async function fetchOrders() {
        loading.value = true;
        try {
            const { data } = await getOrders();
            orders.value = data;
        } catch (err) {
            error.value = err.response?.data || err.message;
        } finally {
            loading.value = false;
        }
    }

    async function fetchOrder(id) {
        try {
            const { data } = await getOrderById(id);
            currentOrder.value = data;
        } catch (err) {
            error.value = err.response?.data || err.message;
        }
    }

    async function createOrder(orderData) {
        const { data } = await placeOrder(orderData);
        orders.value.unshift(data);
        currentOrder.value = data;
    }

    return {
        orders,
        currentOrder,
        loading,
        error,
        fetchOrders,
        fetchOrder,
        createOrder,
    };
});
