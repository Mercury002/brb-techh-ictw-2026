<script setup lang="ts">
import AppIcon from '../components/AppIcon.vue'
import FigmaArt from '../components/FigmaArt.vue'
import { t } from '../i18n'
</script>

<template>
  <section id="cover" class="section cover">
    <FigmaArt name="cover" fit="cover" />
    <h1 class="cover-logo">
      <AppIcon name="logo" />
      <span class="visually-hidden">BRB-TECH</span>
    </h1>
    <div class="cover-profile">
      <p class="cover-profile-title">{{ t().cover.profile }}</p>
      <p class="cover-profile-year">{{ t().cover.year }}</p>
    </div>
  </section>
</template>

<style scoped>
.cover {
  min-height: 100vh;
  min-height: 100svh;
  display: grid;
  place-items: center;
}

.cover-logo {
  position: relative;
  width: calc(903 * var(--u));
}

.cover-logo :deep(img) {
  width: 100%;
  height: auto;
}

.cover-profile {
  position: absolute;
  left: calc(239 * var(--u));
  bottom: calc(276 * var(--u));
  padding-left: calc(38 * var(--u));
  border-left: max(calc(2.3 * var(--u)), 1px) solid #fff;
  font-family: 'IBM Plex Sans', sans-serif;
  line-height: 1.3;
}

.cover-profile-title {
  font-size: max(calc(56 * var(--u)), 16px);
  font-weight: 200;
}

.cover-profile-year {
  font-size: max(calc(64 * var(--u)), 18px);
  font-weight: 500;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
}

@media (max-width: 1199px) {
  .cover-logo {
    width: min(56vw, 440px);
  }

  .cover-profile {
    left: var(--pad-x);
    bottom: 48px;
    padding-left: 14px;
  }
}

@media (max-width: 767px) {
  .cover-logo {
    width: 72vw;
  }

  .cover-profile {
    bottom: 32px;
  }
}
</style>
