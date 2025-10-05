
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
import { getHomepageData } from "~/services/api/home/homepage"
// import { getHomepageData, getHomepageDataById } from "~/services/api/home/homepage"

export const useHomepageStore = defineStore("homepageStore", () => {
    // all home page data listing 
    const sections = ref([])   // all homepage sections as they come from API
    const loading = ref(false)
    const error = ref(null)
    // single homepage data 
    // const banner = ref(null);
    // const bannerLoading = ref(false)
    // const bannerError = ref(null)

    async function fetchHomepageData() {
        loading.value = true
        error.value = null
        try {
            const res = await getHomepageData()
            console.log('inside response homgepageStore----------->  ', res.data);
            if (res.success) {
                // sections.value = res.data || []
                sections.value = [
                    // { type: "hero", data: res.data.hero || {} },
                    { type: "banner", data: res.data.banners || [] },
                    { type: "categories", data: res.data.categories || [] },
                    { type: "products", data: res.data.featured_products || [] },
                    { type: "promo", data: res.data.promotions || [] },
                    { type: "testimonials", data: res.data.testimonials || [] },
                ]

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

    // async function fetchHomepageDataById(id) {
    //     console.info("🚀 [homepageStore] fetchhomepageDataById:", id)
    //     bannerLoading.value = true
    //     bannerError.value = null
    //     banner.value = null

    //     const response = await getHomepageDataById(id)

    //     if (response.success) {
    //         banner.value = response.data
    //         console.info("✅ [HomepageSingeData] homepageData loaded:", response.data)
    //     } else {
    //         bannerError.value = response
    //         console.error("❌ [HomepageStore] failed to load homepageData:", response)
    //     }

    //     bannerLoading.value = false
    //     return response
    // }

    return {
        // Listing 
        sections,
        loading,
        error,
        fetchHomepageData,

        // Single Data 
        // banner,
        // bannerLoading,
        // bannerError,
        // getHomepageDataById
    }
})
