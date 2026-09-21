<script setup lang="ts">
import AppIcon from '../components/AppIcon.vue'
import FigmaImg from '../components/FigmaImg.vue'
import type { images } from '../figma/images'
import { t } from '../i18n'

type AppCard = 'fintech' | 'ai' | 'social' | 'outsourcing' | 'b2b'
type Img = keyof typeof images

// `leaf` is a vector icon, everything else is a raster app icon
const apps: Record<AppCard, (Img | 'leaf')[]> = {
  fintech: ['app-biznes', 'app-credit', 'app-superapp', 'app-smile'],
  ai: ['app-ailab', 'app-findiag', 'app-aicall', 'app-voicepay'],
  social: ['leaf', 'app-buyurtmam', 'app-biznesim'],
  outsourcing: ['app-dev', 'app-audit', 'app-consulting'],
  b2b: ['app-crm', 'app-hrm', 'app-edo'],
}

const bankIcons = ['user-group-02', 'pie-chart-08', 'analytics-up', 'alert-square']
</script>

<template>
  <section id="directions" class="section directions">
    <span class="directions-glow" />
    <h2 class="display">
      <span class="tx-silver">{{ t().directions.title }}</span>
      <template v-if="t().directions.titleAccent">
        {{ ' ' }}<span class="tx-red">{{ t().directions.titleAccent }}</span>
      </template>
    </h2>

    <div class="directions-grid">
      <article
        v-for="key in (['fintech', 'ai', 'social', 'outsourcing', 'b2b'] as const)"
        :key="key"
        class="direction-card glass"
        :class="`direction-${key}`"
      >
        <h3 class="direction-title tx-silver">{{ t().directions[key].title }}</h3>
        <p class="direction-text tx-silver">{{ t().directions[key].text }}</p>
        <ul class="direction-apps" :class="{ 'direction-apps-large': key === 'outsourcing' }">
          <li v-for="(label, i) in t().directions[key].apps" :key="i">
            <AppIcon v-if="apps[key][i] === 'leaf'" name="leaf" class="direction-app-icon" />
            <FigmaImg v-else :name="apps[key][i] as Img" class="direction-app-icon" />
            <span class="direction-app-label tx-silver">{{ label }}</span>
          </li>
        </ul>
      </article>

      <article class="direction-card glass direction-education">
        <h3 class="direction-title tx-silver">{{ t().directions.education.title }}</h3>
        <p class="direction-text tx-silver">{{ t().directions.education.text }}</p>
        <div class="academy">
          <span class="academy-glow" />
          <AppIcon name="academy-leaf" class="academy-leaf" />
          <div class="academy-head">
            <span class="academy-icon">
              <AppIcon name="mortarboard" />
            </span>
            <div>
              <p class="academy-title tx-silver">{{ t().directions.education.academy }}</p>
              <p class="academy-text tx-silver">{{ t().directions.education.academyText }}</p>
            </div>
          </div>
          <ul class="academy-tags">
            <li v-for="(tag, i) in t().directions.education.tags" :key="i">{{ tag }}</li>
          </ul>
        </div>
      </article>

      <div class="directions-logo glass" aria-hidden="true">
        <AppIcon name="logo" />
      </div>

      <article class="direction-card glass direction-bank">
        <h3 class="direction-title tx-silver">{{ t().directions.bank.title }}</h3>
        <p class="direction-text tx-silver">{{ t().directions.bank.text }}</p>
        <ul class="bank-items">
          <li v-for="(item, i) in t().directions.bank.items" :key="i" class="glass">
            <AppIcon :name="bankIcons[i]" class="bank-item-icon" />
            <div>
              <p class="bank-item-title tx-silver">{{ item.title }}</p>
              <p class="bank-item-text tx-silver">{{ item.text }}</p>
            </div>
          </li>
        </ul>
      </article>
    </div>
  </section>
</template>

<style scoped>
.directions-glow {
  position: absolute;
  left: 50%;
  top: 50%;
  width: calc(2153 * var(--u));
  height: calc(2707 * var(--u));
  transform: translate(-50%, -50%);
  background: radial-gradient(closest-side, rgba(227, 6, 19, 0.55), rgba(227, 6, 19, 0.18) 55%, transparent);
  filter: blur(calc(200 * var(--u)));
  pointer-events: none;
}

.directions h2 {
  position: relative;
}

/* 1057 | 48 | 1018 | 48 | 1057: side columns with cards, the logo and the bank card in the middle */
.directions-grid {
  position: relative;
  display: grid;
  grid-template-columns: 1057fr 48fr 1018fr 48fr 1057fr;
  grid-template-rows: repeat(3, auto);
  grid-template-areas:
    'fintech . logo . education'
    'ai . logo . outsourcing'
    'social bank bank bank b2b';
  row-gap: var(--gap-s);
  margin-top: calc(140 * var(--u));
}

.direction-fintech {
  grid-area: fintech;
}

.direction-ai {
  grid-area: ai;
}

.direction-social {
  grid-area: social;
}

.direction-education {
  grid-area: education;
}

.direction-outsourcing {
  grid-area: outsourcing;
}

.direction-b2b {
  grid-area: b2b;
}

.direction-bank {
  grid-area: bank;
  margin: 0 calc(48 * var(--u));
}

.directions-logo {
  grid-area: logo;
  align-self: center;
  justify-self: center;
  display: grid;
  place-items: center;
  width: calc(738 * var(--u));
  aspect-ratio: 738 / 764;
  border-radius: 50%;
  background: rgba(227, 6, 19, 0.35);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.9),
    inset 2px 2px 0 rgba(255, 255, 255, 0.28);
}

.directions-logo :deep(img) {
  width: 85%;
  height: auto;
  filter: drop-shadow(0 0 calc(30 * var(--u)) rgba(255, 60, 60, 0.6));
}

.direction-card {
  display: flex;
  flex-direction: column;
  min-height: calc(530 * var(--u));
  padding: var(--gap-s);
  border-radius: var(--radius-m);
}

.direction-title {
  font-size: max(calc(36 * var(--u)), 15px);
  font-weight: 500;
  line-height: 1.24;
}

.direction-text {
  margin-top: calc(12 * var(--u));
  font-size: max(calc(24 * var(--u)), 11px);
  font-weight: 500;
  line-height: 1.24;
}

.direction-apps {
  display: flex;
  justify-content: space-between;
  gap: var(--gap-xs);
  margin-top: auto;
  padding-top: calc(82 * var(--u));
}

.direction-apps li {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(24 * var(--u));
  width: calc(185 * var(--u));
  text-align: center;
}

.direction-app-icon {
  width: var(--icon);
  height: var(--icon);
  border-radius: var(--radius-s);
}

.direction-apps-large .direction-app-icon {
  width: calc(var(--icon) * 1.28);
  height: calc(var(--icon) * 1.28);
}

.direction-apps-large li {
  gap: calc(8 * var(--u));
}

.direction-app-label {
  font-size: max(calc(26 * var(--u)), 11px);
  font-weight: 500;
  line-height: 1.24;
}

/* BRB-TECH Academy card */
.academy {
  position: relative;
  margin-top: auto;
  padding: var(--gap-s);
  overflow: hidden;
  border: max(calc(1.3 * var(--u)), 1px) solid rgba(225, 18, 33, 0.4);
  border-radius: var(--radius-s);
  background: linear-gradient(100.5deg, #2a0c10 1.2%, #12080a 54.9%, #1c0a0d 98.8%);
  box-shadow: inset 0 0 calc(52 * var(--u)) rgba(180, 10, 20, 0.25);
}

.academy-glow {
  position: absolute;
  right: -40%;
  top: -150%;
  width: 120%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(closest-side, rgba(225, 18, 33, 0.4), transparent 70%);
  pointer-events: none;
}

.academy-leaf {
  position: absolute;
  left: 60%;
  top: 2.5%;
  width: 29.8%;
  height: auto;
  opacity: 0.35;
}

.academy-head {
  position: relative;
  display: flex;
  align-items: center;
  gap: calc(26 * var(--u));
}

.academy-icon {
  display: grid;
  flex: none;
  place-items: center;
  width: var(--icon);
  height: var(--icon);
  border-radius: calc(26 * var(--u));
  background: linear-gradient(160deg, #ff2c3f 8.5%, #c60f22 91.5%);
  box-shadow: 0 calc(10.5 * var(--u)) calc(31.5 * var(--u)) rgba(198, 15, 34, 0.45);
}

.academy-icon :deep(img) {
  width: 57%;
}

.academy-title {
  font-size: max(calc(36 * var(--u)), 15px);
  font-weight: 500;
  line-height: 1.24;
}

.academy-text {
  margin-top: calc(11 * var(--u));
  font-size: max(calc(22 * var(--u)), 11px);
  font-weight: 500;
  line-height: 1.24;
}

.academy-tags {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: calc(11 * var(--u));
  margin-top: calc(39 * var(--u));
}

.academy-tags li {
  padding: calc(9 * var(--u)) calc(19 * var(--u));
  border: max(calc(1.3 * var(--u)), 1px) solid rgba(225, 18, 33, 0.45);
  border-radius: 999px;
  background: rgba(225, 18, 33, 0.12);
  font-size: max(calc(18 * var(--u)), 10px);
  font-weight: 500;
  line-height: 1.24;
}

/* bank management systems */
.bank-items {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  grid-auto-flow: column;
  gap: calc(16 * var(--u));
  margin-top: auto;
  padding-top: calc(40 * var(--u));
}

.bank-items li {
  display: flex;
  align-items: center;
  gap: var(--gap-xs);
  min-height: calc(152 * var(--u));
  padding: var(--gap-xs);
  border-radius: var(--radius-s);
}

.bank-item-icon {
  flex: none;
  width: calc(64 * var(--u));
  height: calc(64 * var(--u));
}

.bank-item-title {
  font-size: max(calc(22 * var(--u)), 11px);
  font-weight: 500;
  line-height: 1.24;
}

.bank-item-text {
  margin-top: calc(4 * var(--u));
  font-size: max(calc(18 * var(--u)), 10px);
  font-weight: 400;
  line-height: 1.24;
}

@media (max-width: 1199px) {
  .directions-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      'fintech education'
      'ai outsourcing'
      'social b2b'
      'bank bank';
    gap: 16px;
    margin-top: 40px;
  }

  .direction-bank {
    margin: 0;
  }

  .directions-logo {
    display: none;
  }

  .direction-card {
    min-height: 0;
  }

  .direction-apps {
    padding-top: 28px;
  }

  .direction-apps li {
    gap: 8px;
    width: auto;
    flex: 1;
  }

  .academy {
    margin-top: 24px;
    padding: 18px;
  }

  .academy-icon {
    width: 52px;
    height: 52px;
    border-radius: 12px;
  }

  .academy-tags {
    gap: 6px;
    margin-top: 16px;
  }

  .academy-tags li {
    padding: 4px 10px;
  }

  .bank-items {
    gap: 10px;
    padding-top: 20px;
  }

  .bank-items li {
    min-height: 0;
    padding: 14px;
  }

  .bank-item-icon {
    width: 36px;
    height: 36px;
  }

  .bank-item-title {
    font-size: 14px;
  }

  .bank-item-text {
    font-size: 12px;
  }
}

@media (max-width: 767px) {
  .directions-grid {
    grid-template-columns: 1fr;
    grid-template-areas: 'fintech' 'ai' 'social' 'bank' 'b2b' 'education' 'outsourcing';
  }

  .direction-apps {
    gap: 6px;
  }

  .direction-app-icon {
    width: 56px;
    height: 56px;
  }

  .direction-apps-large .direction-app-icon {
    width: 64px;
    height: 64px;
  }

  .bank-items {
    grid-template-columns: 1fr;
    grid-auto-flow: row;
  }
}
</style>
