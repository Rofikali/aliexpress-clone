<!-- <template>
    <div class="max-w-[700px] w-full md:block hidden">
        <div class="relative">
            <div class="flex items-center border-2 border-[#FF4646] rounded-md w-full">
                <input class="w-full placeholder-gray-400 text-sm pl-3 focus:outline-none"
                    placeholder="kitchen accessories" type="text" v-model="searchItem">
                <Icon v-if="isSearching" name="eos-icons:loading" size="25" class="mr-2" />
                <button class="flex items-center h-[100%] p-1.5 px-2 bg-[#FF4646]">
                    <Icon name="ph:magnifying-glass" size="20" color="#ffffff" />
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    searchItem: {
        type: String,
        required: false, // true
        default: () => null
    },
    isSearching: {
        type: Boolean,
        required: false, // true
        default: () => false
    }
})

</script>

<style scoped></style> -->

<template>
    <div class="w-full">
        <label :for="id" class="sr-only">{{ ariaLabel }}</label>
        <div class="flex items-stretch border-2 rounded-md w-full" :class="borderClass">
            <input :id="id" v-model="localValue" :placeholder="placeholder" type="text"
                class="w-full text-sm pl-3 py-2 focus:outline-none" @input="emitUpdate" :autocomplete="autocomplete"
                :autocapitalize="autocapitalize" :spellcheck="spellcheck" :aria-label="ariaLabel" />
            <button type="button" class="px-3 flex items-center" :class="buttonClass" @click="$emit('submit')"
                :aria-label="buttonAriaLabel">
                <slot name="icon">
                    <Icon name="ph:magnifying-glass" size="20" />
                </slot>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    modelValue: { type: String, default: '' },
    placeholder: { type: String, default: 'Search…' },
    ariaLabel: { type: String, default: 'Search' },
    buttonAriaLabel: { type: String, default: 'Submit search' },
    id: { type: String, default: 'search-input' },
    // styling hooks (Tailwind classes)
    borderClass: { type: String, default: 'border-[#FF4646]' },
    buttonClass: { type: String, default: 'bg-[#FF4646] text-white' },
    autocomplete: { type: String, default: 'off' },
    autocapitalize: { type: String, default: 'none' },
    spellcheck: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'submit'])
const localValue = ref(props.modelValue)

function emitUpdate() {
    emit('update:modelValue', localValue.value)
}

watch(() => props.modelValue, (v) => { if (v !== localValue.value) localValue.value = v })
</script>

<style scoped>
/* optional: keep it minimal; styling is mostly via Tailwind classes passed via props */
</style>
