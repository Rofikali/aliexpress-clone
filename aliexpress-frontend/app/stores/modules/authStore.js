// // stores/modules/authStore.js
// import { defineStore } from "pinia";
// import { ref, computed } from "vue";
// import { useApi } from "~/composables/core/base";

// export const useAuthStore = defineStore("auth", () => {
//     // ----- state -----
//     const user = ref(null);
//     const tokens = ref(null); // { access, refresh }
//     const loading = ref(false);
//     const error = ref(null);
//     const isHydrated = ref(false);

//     // ----- computed -----
//     const isAuthenticated = computed(() => !!user.value);

//     // ----- helpers -----
//     function normalizeError(err) {
//         return (
//             err?.response?.data?.message ||
//             err?.response?.data?.detail ||
//             err?.response?.data ||
//             err?.message ||
//             "Something went wrong"
//         ).toString();
//     }

//     function setAccessToken(access) {
//         if (!tokens.value) tokens.value = { access };
//         else tokens.value.access = access;
//     }

//     function setUser(u) {
//         user.value = u;
//     }

//     // ----- actions -----
//     async function loginUser(email, password) {
//         loading.value = true;
//         error.value = null;
//         try {
//             const { data } = await useApi("/auth/login/", {
//                 method: "POST",
//                 body: { email, password },
//             });

//             user.value = data.profile || data.user || null;
//             tokens.value = data.tokens || null;

//             return data;
//         } catch (err) {
//             error.value = normalizeError(err);
//             throw err;
//         } finally {
//             loading.value = false;
//             isHydrated.value = true;
//         }
//     }

//     async function registerUser(userData) {
//         loading.value = true;
//         error.value = null;
//         try {
//             const { data } = await useApi("/auth/register/", {
//                 method: "POST",
//                 body: userData,
//             });

//             if (data?.tokens) {
//                 user.value = data.profile || data.user || null;
//                 tokens.value = data.tokens;
//             } else {
//                 // fallback: auto-login
//                 await loginUser(userData.email, userData.password);
//             }

//             return data;
//         } catch (err) {
//             error.value = normalizeError(err);
//             throw err;
//         } finally {
//             loading.value = false;
//             isHydrated.value = true;
//         }
//     }

//     async function fetchProfile() {
//         loading.value = true;
//         error.value = null;
//         try {
//             const { data } = await useApi("/profile/", { method: "GET" });
//             user.value = data || null;
//             return data;
//         } catch (err) {
//             error.value = normalizeError(err);
//             user.value = null;
//             throw err;
//         } finally {
//             loading.value = false;
//         }
//     }

//     async function checkAuth() {
//         loading.value = true;
//         try {
//             const { data } = await useApi("/profile/", { method: "GET" });
//             user.value = data?.user || data?.profile || null;
//             isHydrated.value = true;
//             return user.value;
//         } catch (err) {
//             user.value = null;
//             isHydrated.value = true;
//             return null;
//         } finally {
//             loading.value = false;
//         }
//     }

//     async function logoutUser() {
//         loading.value = true;
//         try {
//             await useApi("/logout/", { method: "POST", body: { refresh: tokens.value?.refresh } });
//         } catch (e) {
//             console.warn("logout error", e);
//         } finally {
//             user.value = null;
//             tokens.value = null;
//             loading.value = false;
//             isHydrated.value = true;
//         }
//     }

//     return {
//         // state
//         user,
//         tokens,
//         loading,
//         error,
//         isHydrated,

//         // computed
//         isAuthenticated,

//         // actions
//         loginUser,
//         registerUser,
//         fetchProfile,
//         checkAuth,
//         logoutUser,

//         // helpers
//         setAccessToken,
//         setUser,
//     };
// });



// stores/modules/authStore.js
import { defineStore } from "pinia"
import { AuthService } from "~/services/api/auth"

export const useAuthStore = defineStore("auth", () => {
    const user = ref(null)
    const tokens = ref(null)
    const loading = ref(false)
    const errors = ref(null)

    async function register(payload) {
        loading.value = true
        errors.value = null
        try {
            const res = await AuthService.register(payload)
            if (res.success) {
                tokens.value = res.data.tokens
                user.value = res.data.profile
            } else {
                errors.value = res.errors
            }
            return res
        } finally {
            loading.value = false
        }
    }

    async function login(payload) {
        loading.value = true
        console.log('loading true authStore ', loading.value);
        errors.value = null
        try {
            const res = await AuthService.login(payload)
            if (res.success) {
                tokens.value = res.data.tokens
                user.value = res.data.profile
            } else {
                errors.value = res.errors
            }
            return res
        } finally {
            loading.value = false
            console.log('loading falsee authStore ', loading.value);
        }
    }

    function logout() {
        user.value = null
        tokens.value = null
    }

    function setAccessToken(token) {
        if (tokens.value) {
            tokens.value.access = token
        }
    }

    return { user, tokens, loading, errors, register, login, logout, setAccessToken }
})
