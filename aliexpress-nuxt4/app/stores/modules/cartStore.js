// stores/modules/cartStore.js
import { defineStore } from "pinia";
import {
    getCart,
    addToCart,
    updateCartItem,
    removeFromCart,
} from "~/services/api/cart";

export const useCartStore = defineStore("cart", () => {
    const cart = ref([]);
    const loading = ref(false);
    const error = ref(null);

    async function fetchCart() {
        loading.value = true;
        try {
            const { data } = await getCart();
            cart.value = data.items || [];
        } catch (err) {
            error.value = err.response?.data || err.message;
        } finally {
            loading.value = false;
        }
    }

    async function addItem(productId, quantity = 1) {
        const { data } = await addToCart(productId, quantity);
        cart.value.push(data);
    }

    async function updateItem(itemId, quantity) {
        const { data } = await updateCartItem(itemId, quantity);
        cart.value = cart.value.map((item) =>
            item.id === itemId ? data : item
        );
    }

    async function removeItem(itemId) {
        await removeFromCart(itemId);
        cart.value = cart.value.filter((item) => item.id !== itemId);
    }

    return {
        cart,
        loading,
        error,
        fetchCart,
        addItem,
        updateItem,
        removeItem,
    };
});
