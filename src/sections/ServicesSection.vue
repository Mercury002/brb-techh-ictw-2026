<script setup lang="ts">
import AppIcon from '../components/AppIcon.vue'
import FigmaImg from '../components/FigmaImg.vue'
import { t } from '../i18n'

type CardKey = keyof ReturnType<typeof t>['services']['cards']

const cards: { key: CardKey; image?: 'service-phone' | 'service-card' | 'service-api' }[] = [
  { key: 'design' },
  { key: 'product', image: 'service-phone' },
  { key: 'quality' },
  { key: 'digital', image: 'service-card' },
  { key: 'engineering', image: 'service-api' },
]
</script>

<template>
  <section id="services" class="section services">
    <h2 class="display">
      <span class="tx-silver">{{ t().services.title }}</span>
      <template v-if="t().services.titleAccent">
        {{ ' ' }}<span class="tx-red">{{ t().services.titleAccent }}</span>
      </template>
    </h2>
    <p class="services-subtitle tx-silver">{{ t().services.subtitle }}</p>

    <div class="services-grid">
      <article v-for="card in cards" :key="card.key" class="service-card" :class="`service-${card.key}`">
        <span v-if="card.key === 'design' || card.key === 'quality' || card.key === 'digital'" class="fg-noise service-noise" />
        <FigmaImg v-if="card.image" :name="card.image" class="service-image" />
        <div class="service-body">
          <h3 class="service-title tx-silver">{{ t().services.cards[card.key].title }}</h3>
          <p class="service-text tx-silver">{{ t().services.cards[card.key].text }}</p>
          <ul class="service-items">
            <li v-for="(item, i) in t().services.cards[card.key].items" :key="i">
              <AppIcon name="bullet" class="service-bullet" />
              <div>
                <p class="service-item-title tx-silver">{{ item.title }}</p>
                <p class="service-item-text tx-silver">{{ item.text }}</p>
              </div>
            </li>
          </ul>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.services-subtitle {
  width: calc(1970 * var(--u));
  max-width: 100%;
  margin-top: calc(32 * var(--u));
  font-size: max(calc(50.5 * var(--u)), 16px);
  font-weight: 500;
  line-height: 1.24;
}

/* column tracks reproduce the Figma card edges: 789 | 1602 | 789 and 1602 | 1602 with 24px gutters */
.services-grid {
  display: grid;
  grid-template-columns: 789fr 24fr 789fr 24fr 789fr 24fr 789fr;
  grid-template-areas:
    'design . product product product . quality'
    'digital digital digital . engineering engineering engineering';
  row-gap: var(--gap-xs);
  margin-top: calc(155 * var(--u));
}

.service-design {
  grid-area: design;
}

.service-product {
  grid-area: product;
}

.service-quality {
  grid-area: quality;
}

.service-digital {
  grid-area: digital;
}

.service-engineering {
  grid-area: engineering;
}

.service-card {
  --stroke: max(calc(2.3 * var(--u)), 1px);

  position: relative;
  display: flex;
  min-height: calc(735 * var(--u));
  padding: calc(55 * var(--u));
  border-radius: var(--radius-l);
  isolation: isolate;
}

/* gradient border */
.service-card::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 2;
  padding: var(--stroke);
  border-radius: inherit;
  background: var(--border, none);
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.service-noise {
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  opacity: 0.12;
}

.service-design {
  --border: linear-gradient(150.9deg, #e52c15 27.6%, #7f180c 87.1%);

  background: linear-gradient(164.35deg, #ff1d00 -8.9%, #000 50%, #000 66.1%, #b70003 113.65%);
}

.service-product,
.service-engineering {
  --border: linear-gradient(127.7deg, rgba(229, 42, 18, 0.8) -5.8%, rgba(127, 23, 10, 0.97) 44.2%);
}

.service-quality {
  background: linear-gradient(153.1deg, rgba(229, 42, 18, 0.8) -19.5%, rgba(54, 1, 10, 0.97) 93.1%);
}

.service-digital {
  --border: linear-gradient(131.5deg, #e52c15 27.8%, #7f180c 75.5%);

  overflow: hidden;
  background: radial-gradient(
    131.5% 383.6% at 14.8% -41.2%,
    #ef0000 8.3%,
    #ed0000 19.5%,
    #000 42.9%,
    #000 60.2%,
    #860000 70.7%
  );
}

.service-body {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.service-title {
  font-size: var(--fs-card-title);
  font-weight: 500;
  line-height: 1.24;
}

.service-text {
  margin-top: calc(20 * var(--u));
  font-size: var(--fs-card-text);
  font-weight: 400;
  line-height: 1.24;
}

.service-product .service-text,
.service-digital .service-text {
  max-width: calc(1192 * var(--u));
}

.service-engineering .service-body {
  max-width: calc(946 * var(--u));
}

.service-items {
  display: flex;
  flex-direction: column;
  gap: calc(27 * var(--u));
  margin-top: auto;
  padding-top: calc(25 * var(--u));
}

.service-items li {
  display: flex;
  gap: calc(18 * var(--u));
}

.service-bullet {
  flex: none;
  width: calc(23 * var(--u));
  height: calc(23 * var(--u));
  margin-top: calc(14 * var(--u));
}

.service-item-title {
  font-size: var(--fs-item-title);
  font-weight: 500;
  line-height: 1.24;
}

.service-item-text {
  margin-top: calc(8 * var(--u));
  font-size: var(--fs-card-text);
  font-weight: 400;
  line-height: 1.24;
}

.service-image {
  position: absolute;
  z-index: 1;
  height: auto;
  pointer-events: none;
}

.service-product .service-image {
  left: 55.06%;
  top: -36.7%;
  width: 51.9%;
}

.service-digital .service-image {
  left: 61%;
  top: 5.4%;
  width: 45.4%;
}

.service-engineering .service-image {
  left: 50.2%;
  top: -20.4%;
  width: 54.1%;
}

@media (max-width: 1199px) {
  .services-subtitle {
    width: auto;
  }

  .service-product .service-text,
  .service-digital .service-text {
    max-width: none;
  }

  .services-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      'design quality'
      'product product'
      'digital digital'
      'engineering engineering';
    gap: 16px;
    row-gap: 16px;
    margin-top: 40px;
  }

  .service-card {
    min-height: 0;
    padding: 28px;
  }

  .service-text {
    margin-top: 10px;
  }

  .service-items {
    gap: 14px;
    padding-top: 24px;
  }

  .service-items li {
    gap: 10px;
  }

  .service-bullet {
    width: 10px;
    height: 10px;
    margin-top: 5px;
  }

  .service-item-text {
    margin-top: 4px;
  }

  .service-product,
  .service-digital,
  .service-engineering {
    min-height: 320px;
  }

  .service-product .service-body,
  .service-digital .service-body,
  .service-engineering .service-body {
    max-width: 58%;
  }

  .service-product .service-image {
    left: auto;
    right: 2%;
    top: -12%;
    width: 36%;
  }

  .service-digital .service-image {
    left: auto;
    right: -6%;
    top: 8%;
    width: 42%;
  }

  .service-engineering .service-image {
    left: auto;
    right: -4%;
    top: -6%;
    width: 44%;
  }
}

@media (max-width: 767px) {
  .services-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      'design'
      'product'
      'quality'
      'digital'
      'engineering';
  }

  .service-card {
    padding: 22px;
  }

  .service-product,
  .service-digital,
  .service-engineering {
    min-height: 0;
    padding-top: 150px;
  }

  .service-product .service-body,
  .service-digital .service-body,
  .service-engineering .service-body {
    max-width: none;
  }

  .service-product .service-image {
    right: 4%;
    top: -40px;
    width: 42%;
  }

  .service-digital .service-image {
    right: -4%;
    top: -12px;
    width: 46%;
  }

  .service-engineering .service-image {
    right: 0;
    top: -24px;
    width: 46%;
  }
}
</style>
