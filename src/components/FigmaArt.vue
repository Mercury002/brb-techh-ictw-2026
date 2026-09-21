<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import FigmaNode from './FigmaNode.vue'
import type { Art } from '../figma/types'

const props = withDefaults(
  defineProps<{
    name: string
    /** `width`: scale to the element width (height follows); `cover`: fill the element box */
    fit?: 'width' | 'cover'
  }>(),
  { fit: 'width' },
)

const loaders = import.meta.glob<Art>('../figma/art/*.json', { import: 'default' })

const art = shallowRef<Art>()
const el = ref<HTMLElement>()
const box = ref({ w: 0, h: 0 })
let observer: ResizeObserver | undefined

watch(
  () => props.name,
  async (name) => {
    art.value = await loaders[`../figma/art/${name}.json`]()
  },
  { immediate: true },
)

onMounted(() => {
  observer = new ResizeObserver(([entry]) => {
    box.value = { w: entry.contentRect.width, h: entry.contentRect.height }
  })
  observer.observe(el.value!)
})
onBeforeUnmount(() => observer?.disconnect())

const style = computed(() => {
  const a = art.value
  if (!a || !box.value.w) return { display: 'none' }
  if (props.fit === 'width') {
    const s = box.value.w / a.w
    return { transform: `scale(${s})` }
  }
  const s = Math.max(box.value.w / a.w, box.value.h / a.h)
  return {
    transform: `translate(${(box.value.w - a.w * s) / 2}px, ${(box.value.h - a.h * s) / 2}px) scale(${s})`,
  }
})
</script>

<template>
  <div
    ref="el"
    class="figma-art"
    :class="`fit-${fit}`"
    :style="fit === 'width' && art ? { aspectRatio: `${art.w} / ${art.h}` } : undefined"
    aria-hidden="true"
  >
    <div v-if="art" class="figma-art-stage" :style="style">
      <FigmaNode :node="art.root" />
    </div>
  </div>
</template>

<style scoped>
.figma-art {
  position: relative;
  overflow: hidden;
  pointer-events: none;
}

.figma-art.fit-cover {
  position: absolute;
  inset: 0;
}

.figma-art-stage {
  position: absolute;
  left: 0;
  top: 0;
  transform-origin: 0 0;
}
</style>
