<script setup lang="ts">
import { images } from '../figma/images'

const props = defineProps<{ name: keyof typeof images; alt?: string }>()

const img = images[props.name]
</script>

<template>
  <img
    :src="img.src"
    :alt="alt ?? ''"
    :width="img.w"
    :height="img.h"
    :style="{ objectFit: img.fit }"
    loading="lazy"
    decoding="async"
    draggable="false"
  />
</template>
