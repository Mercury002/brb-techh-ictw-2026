<script setup lang="ts">
import { LOCALES, locale } from '../i18n'
</script>

<template>
  <nav class="lang-switcher" aria-label="Language">
    <button
      v-for="l in LOCALES"
      :key="l"
      type="button"
      :class="{ active: l === locale }"
      :aria-pressed="l === locale"
      @click="locale = l"
    >
      {{ l.toUpperCase() }}
    </button>
  </nav>
</template>

<style scoped>
.lang-switcher {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10;
  display: flex;
  gap: 4px;
  padding: 4px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: inset 1px 1px 0 rgba(255, 255, 255, 0.25);
}

button {
  padding: 6px 12px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: #fff;
  font: 500 13px/1 'Unbounded', sans-serif;
  cursor: pointer;
}

button.active {
  background: #e30613;
}

@media (max-width: 767px) {
  .lang-switcher {
    top: 12px;
    right: 12px;
    padding: 3px;
    gap: 2px;
  }

  button {
    padding: 5px 9px;
    font-size: 11px;
  }
}
</style>
