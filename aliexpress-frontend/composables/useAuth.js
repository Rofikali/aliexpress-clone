import { useCookie } from '#app'

export function useAuth() {
    const token = useCookie('token') // Automatically handles SSR & CSR
    const user = ref(null)

    // Login
    async function login(credentials) {
        try {
            const { data, error } = await useFetch('/api/auth/login', {
                method: 'POST',
                body: credentials
            })

            if (error.value) throw error.value

            token.value = data.value?.access // Save JWT to cookie
            await getUser() // Load user after login
        } catch (err) {
            console.error('Login failed:', err)
            throw err
        }
    }

    // Logout
    function logout() {
        token.value = null
        user.value = null
    }

    // Fetch current user
    async function getUser() {
        if (!token.value) {
            user.value = null
            return
        }

        try {
            const { data, error } = await useFetch('/api/auth/me', {
                headers: {
                    Authorization: `Bearer ${token.value}`
                }
            })

            if (error.value) throw error.value

            user.value = data.value
        } catch (err) {
            console.error('Failed to fetch user:', err)
            user.value = null
        }
    }

    return {
        token,
        user,
        login,
        logout,
        getUser
    }
}
