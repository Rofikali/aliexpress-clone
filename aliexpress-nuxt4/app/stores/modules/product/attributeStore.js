
import { defineStore } from "pinia"
import { ref } from "vue"      // <<-- ADDED
import { getAttributes, getAttributeById } from "~/services/api/products/attribute"

export const useAttributeStore = defineStore("attributeStore", () => {
    const attributes = ref([])
    const attributeLoading = ref(false)
    const attributeError = ref(null)

    const attributeDetail = ref(null)
    const detailLoading = ref(false)
    const detailError = ref(null)

    // Fetch all attributes for a variant
    async function fetchAttributes(productId, variantId) {
        if (!productId || !variantId) return
        attributeLoading.value = true
        attributeError.value = null
        try {
            const res = await getAttributes(productId, variantId)
            if (res.success) attributes.value = res.data
            else attributeError.value = res
            return res
        } catch (err) {
            attributeError.value = err
            return err
        } finally {
            attributeLoading.value = false
        }
    }

    // Fetch single attribute detail
    async function fetchAttributeById(productId, variantId, attrId) {
        if (!productId || !variantId || !attrId) return
        detailLoading.value = true
        detailError.value = null
        try {
            const res = await getAttributeById(productId, variantId, attrId)
            if (res.success) attributeDetail.value = res.data
            else detailError.value = res
            return res
        } catch (err) {
            detailError.value = err
            return err
        } finally {
            detailLoading.value = false
        }
    }

    return {
        // state
        attributes,
        attributeLoading,
        attributeError,
        attributeDetail,
        detailLoading,
        detailError,
        // actions
        fetchAttributes,
        fetchAttributeById,
    }
})
