<template>
    <div>
<h1>Testimonials</h1>
                <div v-for="item in 5" :key="item.id">
                    <NuxtLink to="/" class="min-w-[170px]">
                        <img width="170" src="/bnr.jpg">
                    </NuxtLink>
                </div>
    </div>
</template>

<script setup>

</script>

<style scoped>

</style>