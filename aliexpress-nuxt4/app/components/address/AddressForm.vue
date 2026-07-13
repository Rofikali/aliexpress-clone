<template>
  <form @submit.prevent="submit">
    <h4>Add New Address</h4>

    <input v-model="form.name" placeholder="Full Name" required />
    <input v-model="form.phone" placeholder="Phone" required />
    <input v-model="form.line1" placeholder="Address Line" required />
    <input v-model="form.city" placeholder="City" required />

    <button type="submit">Save Address</button>
  </form>
</template>

<script setup>
import { reactive } from "vue"
import { useAddress } from "~/composables/address/useAddress"
import { useToastStore } from "~/stores/modules/ui/useToastStore"

const toast = useToastStore()
const { addAddress } = useAddress()

const form = reactive({
  name: "",
  phone: "",
  line1: "",
  city: ""
})

async function submit() {
  try {
    await addAddress(form)
    toast.show("Address added", "success")
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unable to save address"
    toast.show(message, "error")
  }
}
</script>
