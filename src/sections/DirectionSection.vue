<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import FigmaArt from '../components/FigmaArt.vue'
import FigmaImg from '../components/FigmaImg.vue'
import type { images } from '../figma/images'
import { t } from '../i18n'

type Img = keyof typeof images

const props = defineProps<{
  id: 'fintech' | 'education' | 'ai' | 'outsourcing' | 'b2b' | 'bank'
  /** icon file name, or `img:<image>` for raster icons */
  icons: string[]
  /** `grid`: two columns of icon + text; `row`: one row with dividers */
  layout: 'grid' | 'row'
  /** illustration: an art composition or an image, with its box on the Figma page */
  visual: { art?: string; img?: Img; x: number; y: number; w: number }
}>()

const content = computed(() => t()[props.id])
const featuresTitle = computed(() => ('featuresTitle' in content.value ? content.value.featuresTitle : ''))

const visualStyle = computed(() => ({
  '--vx': props.visual.x,
  '--vy': props.visual.y,
  '--vw': props.visual.w,
}))
</script>

<template>
  <section :id="id" class="section section-dark direction" :class="`direction-${layout}`">
    <div class="direction-visual" :style="visualStyle">
      <FigmaArt v-if="visual.art" :name="visual.art" />
      <FigmaImg v-else-if="visual.img" :name="visual.img" />
    </div>

    <h2 class="direction-heading">
      <span class="direction-number tx-red">{{ content.number }}</span>
      <span class="direction-title tx-silver">{{ content.title }}</span>
    </h2>
    <p class="direction-subtitle lead tx-silver">{{ content.subtitle }}</p>
    <span class="direction-line" />
    <div class="direction-text">
      <p v-for="(p, i) in content.paragraphs" :key="i" class="body-text tx-silver">{{ p }}</p>
    </div>

    <h3 v-if="featuresTitle" class="direction-h3 tx-silver">{{ featuresTitle }}</h3>
    <ul class="features" :class="[`features-${layout}`, { 'features-titled': featuresTitle }]">
      <li v-for="(f, i) in content.features" :key="i" class="feature">
        <FigmaImg v-if="icons[i].startsWith('img:')" :name="icons[i].slice(4) as Img" class="feature-icon" />
        <AppIcon v-else :name="icons[i]" class="feature-icon" />
        <div>
          <p class="feature-title tx-silver">{{ f.title }}</p>
          <p class="feature-text tx-silver">{{ f.text }}</p>
        </div>
      </li>
    </ul>

    <h3 class="direction-h3 direction-audience-title tx-silver">{{ content.audienceTitle }}</h3>
    <ul class="direction-audience">
      <li v-for="(a, i) in content.audience" :key="i" class="pill glass">
        <span class="tx-silver">{{ a }}</span>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.direction {
  min-height: max(100vh, calc(2480 * var(--u)));
}

.direction > * {
  position: relative;
}

.direction-visual {
  position: absolute !important;
  left: calc(var(--vx) * var(--u));
  top: calc(var(--vy) * var(--u));
  width: calc(var(--vw) * var(--u));
}

.direction-visual :deep(img) {
  width: 100%;
  height: auto;
}

.direction-heading {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  column-gap: calc(40 * var(--u));
  font-weight: 600;
  line-height: 1.24;
}

.direction-number {
  font-size: var(--fs-number);
}

.direction-title {
  font-size: var(--fs-page-title);
}

.direction-subtitle {
  width: calc(1679 * var(--u));
  margin-top: var(--gap-m);
}

.direction-line {
  display: block;
  width: calc(283 * var(--u));
  height: max(calc(4 * var(--u)), 2px);
  margin: var(--gap-m) 0;
  background: linear-gradient(90deg, #e52c15 27.9%, #7f180c 65.6%);
}

.direction-text {
  display: flex;
  flex-direction: column;
  gap: var(--gap-s);
  width: calc(1679 * var(--u));
}

.direction-h3 {
  margin-top: var(--gap-m);
  font-size: var(--fs-h3);
  font-weight: 500;
  line-height: 1.24;
}

.features {
  margin-top: var(--gap-m);
}

.features-titled {
  margin-top: var(--gap-s);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, calc(659 * var(--u)));
  grid-template-rows: repeat(3, auto);
  grid-auto-flow: column;
  column-gap: calc(160 * var(--u));
  row-gap: var(--gap-s);
}

.features-grid .feature {
  display: flex;
  align-items: center;
  gap: var(--gap-xs);
}

.features-row {
  display: flex;
  column-gap: var(--gap-s);
}

.features-row .feature {
  display: flex;
  flex-direction: column;
  gap: var(--gap-xs);
  max-width: calc(500 * var(--u));
}

.features-row .feature + .feature {
  padding-left: var(--gap-s);
  border-left: 1px solid #fff;
}

.feature-icon {
  flex: none;
  width: var(--icon);
  height: var(--icon);
  object-fit: contain;
}

.feature-title {
  font-size: var(--fs-feature-title);
  font-weight: 500;
  line-height: 1.24;
}

.feature-text {
  margin-top: calc(8 * var(--u));
  font-size: var(--fs-feature-text);
  font-weight: 400;
  line-height: 1.24;
}

.direction-audience {
  display: flex;
  flex-wrap: wrap;
  gap: calc(32 * var(--u));
  margin-top: var(--gap-s);
}

/* the illustration sits to the right of the whole page: keep the pills in the text column */
.direction-grid .direction-audience {
  max-width: calc(1740 * var(--u));
}

@media (max-width: 1199px) {
  .direction {
    display: flex;
    flex-direction: column;
    min-height: 0;
  }

  .direction-visual {
    position: relative !important;
    order: 5;
    left: auto;
    top: auto;
    width: min(100%, 640px);
    margin: 32px auto 0;
  }

  .direction-heading,
  .direction-subtitle,
  .direction-line,
  .direction-text {
    order: 1;
  }

  .direction-heading {
    column-gap: 16px;
  }

  .direction-subtitle,
  .direction-text {
    width: auto;
  }

  .direction-h3,
  .features {
    order: 6;
  }

  .direction-audience-title,
  .direction-audience {
    order: 7;
  }

  .features-grid {
    grid-template-columns: 1fr 1fr;
    column-gap: 32px;
  }

  .features-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 28px 24px;
  }

  .features-row .feature {
    max-width: none;
  }

  .features-row .feature + .feature {
    padding-left: 0;
    border-left: 0;
  }

  .feature-text {
    margin-top: 4px;
  }

  .direction-audience {
    gap: 10px;
  }

  .direction-grid .direction-audience {
    max-width: none;
  }
}

@media (max-width: 767px) {
  .features-grid {
    grid-template-columns: 1fr;
    grid-template-rows: none;
    grid-auto-flow: row;
  }

  .features-row {
    grid-template-columns: 1fr 1fr;
    gap: 24px 16px;
  }

  .direction-audience {
    gap: 8px;
  }
}
</style>
