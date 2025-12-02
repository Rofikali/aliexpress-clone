// stores/modules/wishlistStore.js
import { defineStore } from "pinia";
import { getWishlist, addToWishlist, removeFromWishlist } from "~/services/api/wishlist";

export const useWishlistStore = defineStore("wishlist", () => {
    const wishlist = ref([]);
    const loading = ref(false);
    const error = ref(null);

    async function fetchWishlist() {
        try {
            const { data } = await getWishlist();
            wishlist.value = data;
        } catch (err) {
            error.value = err.response?.data || err.message;
        }
    }

    async function addItem(productId) {
        const { data } = await addToWishlist(productId);
        wishlist.value.push(data);
    }

    async function removeItem(productId) {
        await removeFromWishlist(productId);
        wishlist.value = wishlist.value.filter((item) => item.id !== productId);
    }

    return {
        wishlist,
        loading,
        error,
        fetchWishlist,
        addItem,
        removeItem,
    };
});
