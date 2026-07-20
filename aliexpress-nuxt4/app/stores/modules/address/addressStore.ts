import { defineStore } from "pinia"
import { ref } from "vue"
import { fetchAddresses, createAddress } from "~/services/api/address/address.service"

export const useAddressStore = defineStore("address", () => {
    const addresses = ref<any[]>([])
    const selectedAddress = ref<any>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function loadAddresses() {
        loading.value = true
        try {
            const res = await fetchAddresses()
            if (!res.success) throw new Error(res.message || "Unable to load addresses")
            addresses.value = res.data || []
        } catch (e: any) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    async function addAddress(payload: any) {
        const res = await createAddress(payload)
        if (!res.success) throw new Error(res.message || "Unable to add address")
        addresses.value.push(res.data)
        selectedAddress.value = res.data
    }

    return {
        addresses,
        selectedAddress,
        loading,
        error,
        loadAddresses,
        addAddress
    }
})
