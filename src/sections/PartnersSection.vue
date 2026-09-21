<script setup lang="ts">
import { groups, images } from '../figma/images'
import { t } from '../i18n'

type Placed = { src: string; fit: string; box: readonly number[]; aspect: number }

const partner = (name: string) => images[name as keyof typeof images] as unknown as Placed
const cert = (name: string) => images[name as keyof typeof images]

// logo box inside its card, in % of the card (as placed in Figma)
const logoStyle = (p: Placed) => ({
  left: `${p.box[0]}%`,
  top: `${p.box[1]}%`,
  width: `${p.box[2]}%`,
  height: `${p.box[3]}%`,
  objectFit: p.fit as 'cover' | 'contain' | 'fill',
})
</script>

<template>
  <section id="partners" class="section partners">
    <span class="partners-glow" />
    <h2 class="partners-title tx-silver">{{ t().partners.title }}</h2>
    <p class="partners-lead tx-silver">{{ t().partners.lead }}</p>
    <p class="partners-text tx-silver">{{ t().partners.text }}</p>

    <div class="partners-logos">
      <div class="partners-group partners-local">
        <h3 class="partners-label tx-silver">{{ t().partners.local }}</h3>
        <ul class="partners-grid">
          <li v-for="name in groups.partnersLocal" :key="name" :style="{ aspectRatio: partner(name).aspect }">
            <img :src="partner(name).src" alt="" loading="lazy" :style="logoStyle(partner(name))" />
          </li>
        </ul>
      </div>
      <span class="partners-divider" />
      <div class="partners-group partners-intl">
        <h3 class="partners-label tx-red">{{ t().partners.international }}</h3>
        <ul class="partners-grid">
          <li v-for="name in groups.partnersIntl" :key="name" :style="{ aspectRatio: partner(name).aspect }">
            <img :src="partner(name).src" alt="" loading="lazy" :style="logoStyle(partner(name))" />
          </li>
        </ul>
      </div>
    </div>

    <div class="certs">
      <div class="certs-intro">
        <h3 class="certs-title tx-red">{{ t().partners.certsTitle }}</h3>
        <p class="certs-text">{{ t().partners.certsText }}</p>
      </div>
      <ul class="certs-list">
        <li v-for="(c, i) in t().partners.certs" :key="i">
          <span class="certs-img">
            <img
              :src="cert(groups.certs[i]).src"
              :alt="c.title"
              loading="lazy"
              :style="{ width: `calc(${cert(groups.certs[i]).w} * var(--u))` }"
            />
          </span>
          <p class="certs-item-title">{{ c.title }}</p>
          <p class="certs-item-text">{{ c.text }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.partners > * {
  position: relative;
}

.partners-glow {
  position: absolute !important;
  left: calc(-954 * var(--u));
  top: calc(41 * var(--u));
  width: calc(1907 * var(--u));
  height: calc(2397 * var(--u));
  /* soft glow as a many-stop gradient (a css blur of this size renders differently on mobile GPUs) */
  background:
    var(--dither),
    radial-gradient(
      closest-side,
      rgba(227, 6, 19, 0.55),
      rgba(227, 6, 19, 0.45) 20%,
      rgba(227, 6, 19, 0.28) 45%,
      rgba(227, 6, 19, 0.12) 70%,
      rgba(227, 6, 19, 0.03) 88%,
      rgba(227, 6, 19, 0)
    );
  -webkit-mask: radial-gradient(closest-side, #000 60%, transparent);
  mask: radial-gradient(closest-side, #000 60%, transparent);
  pointer-events: none;
}

.partners-title {
  font-size: calc(var(--fs-display) * 1.17);
  font-weight: 600;
  line-height: 1.24;
}

.partners-lead,
.partners-text {
  width: calc(1877 * var(--u));
  max-width: 100%;
  font-size: var(--fs-card-title);
  line-height: 1.24;
}

.partners-lead {
  margin-top: var(--gap-m);
  font-weight: 500;
}

.partners-text {
  width: calc(1661 * var(--u));
  margin-top: calc(21 * var(--u));
  font-weight: 400;
}

.partners-logos {
  display: grid;
  grid-template-columns: 2249fr auto 953fr;
  gap: var(--gap-xs);
  margin-top: var(--gap-m);
}

.partners-label {
  margin-bottom: var(--gap-xs);
  font-size: max(calc(54 * var(--u)), 17px);
  font-weight: 600;
  line-height: 1.24;
}

.partners-intl .partners-label {
  text-align: right;
}

.partners-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--gap-xs) calc(16.3 * var(--u));
}

.partners-intl .partners-grid {
  grid-template-columns: repeat(3, 1fr);
}

.partners-grid li {
  position: relative;
  overflow: hidden;
  border-radius: calc(36.74 * var(--u));
  background: #fff;
}

.partners-grid img {
  position: absolute;
  max-width: none;
}

.partners-divider {
  align-self: end;
  width: max(calc(2.3 * var(--u)), 1px);
  height: calc(451 * var(--u));
  background: #fff;
}

.certs {
  display: grid;
  grid-template-columns: 783fr 2387fr;
  align-items: center;
  gap: calc(20 * var(--u));
  margin-top: var(--gap-m);
  padding: calc(57 * var(--u));
  border-radius: calc(36.74 * var(--u));
  background: #fff;
  color: #000;
}

.certs-title {
  font-size: var(--fs-h2);
  font-weight: 600;
  line-height: 1.24;
}

.certs-text {
  margin-top: calc(27 * var(--u));
  font-size: max(calc(38 * var(--u)), 13px);
  font-weight: 400;
  line-height: 1.24;
}

.certs-list {
  display: grid;
  grid-template-columns: 468fr 553fr 567fr 774fr;
  gap: calc(8 * var(--u));
  text-align: center;
}

.certs-img {
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(290 * var(--u));
  margin-bottom: calc(24 * var(--u));
}

.certs-img img {
  max-height: 100%;
  object-fit: contain;
}

.certs-item-title {
  font-size: max(calc(32 * var(--u)), 13px);
  font-weight: 600;
  line-height: 1.24;
}

.certs-item-text {
  margin-top: calc(17 * var(--u));
  font-size: max(calc(28.15 * var(--u)), 11px);
  font-weight: 400;
  line-height: 1.24;
}

@media (max-width: 1199px) {
  .partners-lead,
  .partners-text {
    width: auto;
  }

  .partners-text {
    margin-top: 10px;
  }

  .partners-logos {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .partners-divider {
    display: none;
  }

  .partners-intl .partners-label {
    text-align: left;
  }

  .partners-grid {
    gap: 10px;
  }

  .partners-grid li {
    border-radius: 16px;
  }

  .certs {
    grid-template-columns: 1fr;
    gap: 28px;
    padding: 28px;
    border-radius: 20px;
  }

  .certs-text {
    margin-top: 10px;
  }

  .certs-list {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }

  .certs-img {
    height: 110px;
    margin-bottom: 10px;
  }

  .certs-img img {
    width: auto !important;
  }

  .certs-item-text {
    margin-top: 6px;
  }
}

@media (max-width: 767px) {
  .partners-local .partners-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .partners-grid li {
    border-radius: 12px;
  }

  .certs {
    padding: 20px;
  }

  .certs-list {
    grid-template-columns: 1fr 1fr;
    gap: 24px 12px;
  }

  .certs-img {
    height: 90px;
  }
}
</style>
