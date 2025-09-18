<template>
    <div id="MainLayout" class="w-full fixed z-50">
        <Navbar />
        <Header />
    </div>

    <Loading v-if="userStore.loading" />

    <div class="lg:pt-[150px] md:pt-[130px] pt-[80px]" />
    <!-- <NuxtLayout> -->
        <slot />
    <!-- </NuxtLayout> -->

    <Footer v-if="!userStore.loading" />
</template>

<script setup>
import Navbar from '~/components/layout/Navbar.vue'
import Header from '~/components/layout/Header.vue'
import Footer from '~/components/layout/Footer.vue'
import Loading from '~/components/Loading.vue'
// import { useUserStore } from '~/stores/user'
import { useAuthStore } from '~/stores/modules/authStore'

// const userStore = useUserStore()
const userStore = useAuthStore()
</script>
