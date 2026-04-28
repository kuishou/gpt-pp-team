<template>
  <label class="tt">
    <input type="checkbox" :checked="modelValue" @change="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)" />
    <span class="tt-box">{{ modelValue ? '[✓]' : '[ ]' }}</span>
    <span class="tt-label"><slot /></span>
  </label>
</template>

<script setup lang="ts">
defineProps<{ modelValue: boolean }>();
defineEmits<{ "update:modelValue": [v: boolean] }>();
</script>

<style scoped>
.tt { display: inline-flex; align-items: center; gap: 8px; cursor: pointer; user-select: none; transition: color 60ms; }
.tt input { display: none; }
.tt-box { color: var(--accent); font-weight: 700; }
.tt:hover .tt-box { text-shadow: 0 0 6px var(--accent); }
.tt-label { font-size: 13px; color: var(--fg-secondary); }
.tt:hover .tt-label { color: var(--fg-primary); }
</style>
