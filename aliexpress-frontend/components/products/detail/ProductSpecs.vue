<template>
  <div class="product-specs">
    <h2>Specifications</h2>
    <table>
      <tbody>
        <tr v-for="(val, key) in specs" :key="key">
          <td class="label">{{ key }}</td>
          <td class="value">{{ val }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  specs: { type: Object, default: () => ({}) }
})
</script>

<style scoped>
.product-specs {
  margin-top: 2rem;
}
.label {
  font-weight: bold;
  width: 150px;
}
</style>
