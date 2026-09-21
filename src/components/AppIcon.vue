<script setup lang="ts">
const icons = import.meta.glob<string>('../assets/icons/*.svg', { eager: true, import: 'default', query: '?url' })

const props = defineProps<{ name: string }>()

const src = icons[`../assets/icons/${props.name}.svg`]
</script>

<template>
  <img :src="src" alt="" class="app-icon" draggable="false" />
</template>
