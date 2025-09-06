// // stores/modules/authStore.js
// import { defineStore } from "pinia";
// import { login, register, getProfile, logout } from "~/services/api/auth";

// export const useAuthStore = defineStore("auth", () => {
//     const user = ref(null);
//     const accessToken = ref(null);
//     const refreshToken = ref(null);
//     const loading = ref(false);
//     const error = ref(null);

//     async function loginUser(email, password) {
//         loading.value = true;
//         error.value = null;
//         try {
//             const { data } = await login(email, password);
//             accessToken.value = data.access;
//             refreshToken.value = data.refresh;
//             await fetchProfile();
//         } catch (err) {
//             error.value = err.response?.data || err.message;
//         } finally {
//             loading.value = false;
//         }
//     }

//     async function registerUser(userData) {
//         loading.value = true;
//         error.value = null;
//         try {
//             await register(userData);
//             // auto-login after register (optional)
//             await loginUser(userData.email, userData.password);
//         } catch (err) {
//             error.value = err.response?.data || err.message;
//         } finally {
//             loading.value = false;
//         }
//     }

//     async function fetchProfile() {
//         try {
//             const { data } = await getProfile();
//             user.value = data;
//         } catch (err) {
//             error.value = err.response?.data || err.message;
//         }
//     }

//     async function logoutUser() {
//         try {
//             await logout();
//         } catch (e) { }
//         user.value = null;
//         accessToken.value = null;
//         refreshToken.value = null;
//     }

//     return {
//         user,
//         accessToken,
//         refreshToken,
//         loading,
//         error,
//         loginUser,
//         registerUser,
//         fetchProfile,
//         logoutUser,
//     };
// });


// stores/modules/authStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useApi } from "~/composables/core/useApi";

export const useAuthStore = defineStore("auth", () => {
    // ----- state -----
    const user = ref(null);
    const tokens = ref(null); // { access, refresh? }
    const loading = ref(false);
    const error = ref(null);
    const isHydrated = ref(false);

    // ----- computed -----
    const isAuthenticated = computed(() => !!user.value);

    // ----- helpers -----
    function normalizeError(err) {
        return (
            err?.response?.data?.message ||
            err?.response?.data?.detail ||
            err?.response?.data ||
            err?.message ||
            "Something went wrong"
        ).toString();
    }

    // ----- actions -----
    async function loginUser(email, password) {
        loading.value = true;
        error.value = null;
        try {
            const { data } = await useApi("/auth/login/", {
                method: "POST",
                body: { email, password },
            });

            user.value = data.profile || data.user || null;
            tokens.value = data.tokens || null;

            // ask backend to set refresh token in HttpOnly cookie
            if (tokens.value?.refresh) {
                try {
                    await useApi("/refresh/", {
                        method: "POST",
                        body: { refresh: tokens.value.refresh },
                    });
                } catch (e) {
                    console.warn("Failed to set refresh cookie:", e);
                }
            }

            return data;
        } catch (err) {
            error.value = normalizeError(err);
            throw err;
        } finally {
            loading.value = false;
            isHydrated.value = true;
        }
    }

    async function registerUser(userData) {
        loading.value = true;
        error.value = null;
        try {
            const { data } = await useApi("/register/", {
                method: "POST",
                body: userData,
            });

            if (data?.tokens) {
                user.value = data.profile || data.user || null;
                tokens.value = data.tokens;
            } else {
                await loginUser(userData.email, userData.password);
            }

            return data;
        } catch (err) {
            error.value = normalizeError(err);
            throw err;
        } finally {
            loading.value = false;
            isHydrated.value = true;
        }
    }

    async function fetchProfile() {
        loading.value = true;
        error.value = null;
        try {
            const { data } = await useApi("/profile/", { method: "GET" });
            user.value = data || null;
            return data;
        } catch (err) {
            error.value = normalizeError(err);
            user.value = null;
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function checkAuth() {
        loading.value = true;
        try {
            const { data } = await useApi("/profile/", { method: "GET" });
            // const { data } = await useApi("/auth/me/", { method: "GET" });
            user.value = data?.user || data?.profile || null;
            isHydrated.value = true;
            return user.value;
        } catch (err) {
            user.value = null;
            isHydrated.value = true;
            return null;
        } finally {
            loading.value = false;
        }
    }

    async function logoutUser() {
        loading.value = true;
        try {
            await useApi("logout/", { method: "POST" });
        } catch (e) {
            console.warn("logout error", e);
        } finally {
            user.value = null;
            tokens.value = null;
            loading.value = false;
            isHydrated.value = true;
        }
    }

    // helpers
    function setAccessToken(access) {
        if (!tokens.value) tokens.value = { access };
        else tokens.value.access = access;
    }
    function setUser(u) {
        user.value = u;
    }

    return {
        // state
        user,
        tokens,
        loading,
        error,
        isHydrated,

        // computed
        isAuthenticated,

        // actions
        loginUser,
        registerUser,
        fetchProfile,
        checkAuth,
        logoutUser,

        // helpers
        setAccessToken,
        setUser,
    };
});
