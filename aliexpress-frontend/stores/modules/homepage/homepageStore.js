
// import { defineStore } from "pinia"
// // import { getAttributes, getAttributeById } from "~/services/api/products/attribute"
// import { getHomepageData } from "~/services/api/homepage"

// export const useHomepageStore = defineStore("homepageStore", () => {
//     // Homepage sections
//     const hero = ref({})
//     const banners = ref([])
//     const categories = ref([])
//     const testimonials = ref([])

//     const loading = ref(false)
//     const error = ref(null)

//     async function fetchHomepageData() {
//         loading.value = true
//         error.value = null
//         try {
//             const res = await getHomepageData()
//             if (res.success) {
//                 hero.value = res.data.hero
//                 banners.value = res.data.banners
//                 categories.value = res.data.categories
//                 testimonials.value = res.data.testimonials
//             } else {
//                 error.value = res
//             }
//             return res
//         } catch (e) {
//             error.value = e
//             return e
//         } finally {
//             loading.value = false
//         }
//     }

//     return {
//         // Homepage sections
//         hero,
//         banners,
//         categories,
//         testimonials,

//         // General
//         loading,
//         error,
//         fetchHomepageData
//     }
// })


import { defineStore } from "pinia"
import { getHomepageData } from "~/services/api/homepage"

export const useHomepageStore = defineStore("homepageStore", () => {
    const sections = ref([])   // all homepage sections as they come from API
    const loading = ref(false)
    const error = ref(null)

    async function fetchHomepageData() {
        loading.value = true
        error.value = null
        try {
            const res = await getHomepageData()
            console.log('inside response ----------->  ', res.data);
            if (res.success) {
                sections.value = res.data || []
            } else {
                error.value = res
            }
            return res
        } catch (e) {
            error.value = e
            return e
        } finally {
            loading.value = false
        }
    }

    return {
        sections,
        loading,
        error,
        fetchHomepageData
    }
})
