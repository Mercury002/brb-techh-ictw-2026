<script setup lang="ts">
import FigmaArt from '../components/FigmaArt.vue'
import FigmaImg from '../components/FigmaImg.vue'
import { t } from '../i18n'

const valueImages = ['value-innovation', 'value-reliability', 'value-flexibility'] as const
</script>

<template>
  <section id="about" class="section about">
    <FigmaArt name="globe" class="about-globe" />

    <div class="about-content">
      <h2 class="display">
        <span class="tx-silver">{{ t().about.title }}</span>
        <template v-if="t().about.titleAccent">
          {{ ' ' }}<span class="tx-red">{{ t().about.titleAccent }}</span>
        </template>
      </h2>
      <div class="about-text">
        <p v-for="(p, i) in t().about.paragraphs" :key="i" class="body-text tx-silver">{{ p }}</p>
      </div>
    </div>

    <div class="about-card glass">
      <div class="about-results">
        <h3 class="about-card-title tx-silver">{{ t().about.resultsTitle }}</h3>
        <ul class="about-stats">
          <li v-for="(s, i) in t().about.stats" :key="i">
            <strong class="about-stat-value tx-silver">{{ s.value }}</strong>
            <span class="about-stat-label tx-silver">{{ s.label }}</span>
          </li>
        </ul>
      </div>
      <div class="about-card-divider" />
      <div class="about-values">
        <h3 class="about-card-title tx-silver">{{ t().about.valuesTitle }}</h3>
        <ul class="about-values-list">
          <li v-for="(v, i) in t().about.values" :key="i">
            <FigmaImg :name="valueImages[i]" class="about-value-img" />
            <span class="about-value-label tx-silver">{{ v }}</span>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: calc(140 * var(--u));
}

.about-globe {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
}

.about-content {
  position: relative;
  width: calc(1730 * var(--u));
}

.about-text {
  display: flex;
  flex-direction: column;
  gap: calc(32 * var(--u));
  margin-top: calc(138 * var(--u));
}

.about-card {
  position: relative;
  display: grid;
  grid-template-columns: 1638fr auto 1285fr;
  gap: var(--gap-m);
  padding: var(--gap-m);
  border-radius: var(--radius-m);
}

.about-card-title {
  font-size: var(--fs-h3);
  font-weight: 600;
  line-height: 1.24;
}

.about-card-divider {
  width: 1px;
  background: #fff;
}

.about-stats {
  display: flex;
  justify-content: space-between;
  margin-top: calc(124 * var(--u));
}

.about-stats li {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  gap: calc(43 * var(--u));
  text-align: center;
}

.about-stats li + li {
  border-left: 1px solid #fff;
}

.about-stat-value {
  font-size: calc(80 * var(--u));
  font-weight: 700;
  line-height: 1.24;
}

.about-stat-label {
  max-width: calc(381 * var(--u));
  font-size: max(calc(32 * var(--u)), 12px);
  font-weight: 300;
  line-height: 1.24;
}

.about-values-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--gap-m);
  margin-top: calc(24 * var(--u));
}

.about-values-list li {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(24 * var(--u));
}

.about-value-img {
  width: calc(300 * var(--u));
  height: calc(300 * var(--u));
}

.about-value-label {
  font-size: max(calc(40 * var(--u)), 13px);
  font-weight: 400;
  line-height: 1.24;
  text-align: center;
}

@media (max-width: 1199px) {
  .about {
    justify-content: flex-start;
    gap: 48px;
  }

  .about-globe {
    left: auto;
    right: -60%;
    top: -60px;
    width: 180%;
    opacity: 0.55;
  }

  .about-content {
    width: auto;
  }

  .about-text {
    gap: 16px;
    margin-top: 32px;
  }

  .about-card {
    grid-template-columns: 1fr;
    padding: 32px;
  }

  .about-card-divider {
    width: auto;
    height: 1px;
  }

  .about-stats {
    margin-top: 28px;
  }

  .about-stats li {
    gap: 10px;
    padding: 0 8px;
  }

  .about-stat-value {
    font-size: 40px;
  }

  .about-stat-label {
    max-width: none;
  }

  .about-values-list {
    gap: 16px;
    margin-top: 20px;
  }

  .about-values-list li {
    gap: 8px;
  }

  .about-value-img {
    width: 120px;
    height: 120px;
  }
}

@media (max-width: 767px) {
  .about-globe {
    right: -70%;
    top: -20px;
    width: 220%;
    opacity: 0.4;
  }

  .about-card {
    padding: 20px;
    gap: 24px;
  }

  .about-stats {
    margin-top: 20px;
  }

  .about-stats li {
    padding: 0 4px;
  }

  .about-stat-value {
    font-size: 28px;
  }

  .about-stat-label {
    font-size: 11px;
  }

  .about-values-list {
    gap: 8px;
  }

  .about-value-img {
    width: 80px;
    height: 80px;
  }

  .about-value-label {
    font-size: 11px;
  }
}
</style>
