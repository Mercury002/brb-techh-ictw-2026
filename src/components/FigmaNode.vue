<script setup lang="ts">
import type { SceneNode } from '../figma/types'

defineOptions({ name: 'FigmaNode' })

defineProps<{ node: SceneNode }>()
</script>

<template>
  <div :style="node.s" :class="node.cl">
    <div v-if="node.h" class="fg-paint" v-html="node.h" />
    <FigmaNode v-for="(child, i) in node.c" :key="i" :node="child" />
  </div>
</template>
