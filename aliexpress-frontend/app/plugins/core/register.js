// import { useUserStore } from "~/stores/user"
// // import { useProfileStore } from "~/EXTRAS/profile"
// import { useProfileStore } from "~/stores/Profile/profile"
// import { useGeneralStore } from "~/stores/general"
import { AuthService } from "~/services/api/auth"

export default defineNuxtPlugin((NuxtApp) => {
    return {
        provide: {
            userStore: useUserStore(),
            profileStore: useProfileStore(),
            generalStore: useGeneralStore()
        },
    }
})