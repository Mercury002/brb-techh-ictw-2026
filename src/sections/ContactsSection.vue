<script setup lang="ts">
import AppIcon from '../components/AppIcon.vue'
import FigmaArt from '../components/FigmaArt.vue'
import FigmaImg from '../components/FigmaImg.vue'
import { t } from '../i18n'
</script>

<template>
  <footer id="contacts" class="section contacts">
    <FigmaArt name="contacts" fit="cover" />
    <div class="contacts-logo">
      <AppIcon name="logo" />
    </div>

    <address class="contacts-list">
      <div>
        <p class="contacts-label tx-silver">{{ t().contacts.addressLabel }}</p>
        <p class="contacts-value">{{ t().contacts.address }}</p>
      </div>
      <div>
        <p class="contacts-label">{{ t().contacts.emailLabel }}</p>
        <a class="contacts-value" :href="`mailto:${t().contacts.email}`">{{ t().contacts.email }}</a>
      </div>
      <div>
        <p class="contacts-label">{{ t().contacts.phoneLabel }}</p>
        <a class="contacts-value" :href="`tel:${t().contacts.phone.replace(/[^\d+]/g, '')}`">{{ t().contacts.phone }}</a>
      </div>
    </address>

    <a class="contacts-qr" href="https://brb-tech.uz" target="_blank" rel="noopener">
      <span class="contacts-qr-frame">
        <AppIcon name="qr-frame" class="contacts-qr-border" />
        <FigmaImg name="qr" class="contacts-qr-code" alt="QR" />
      </span>
      <span class="contacts-value">{{ t().contacts.website }}</span>
    </a>
  </footer>
</template>

<style scoped>
.contacts {
  min-height: 100vh;
  min-height: 100svh;
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-rows: 1fr auto;
  align-items: end;
  gap: var(--gap-m);
}

.contacts-logo {
  position: relative;
  grid-column: 1 / -1;
  align-self: center;
  justify-self: center;
  width: calc(903 * var(--u));
}

.contacts-logo :deep(img) {
  width: 100%;
  height: auto;
}

.contacts-list {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: calc(37 * var(--u));
  padding-bottom: calc(40 * var(--u));
  font-style: normal;
  font-size: max(calc(45.93 * var(--u)), 15px);
  line-height: 1.24;
}

.contacts-label {
  margin-bottom: calc(18 * var(--u));
  font-weight: 400;
}

.contacts-value {
  display: block;
  font-weight: 300;
  color: #fff;
  text-decoration: none;
  white-space: pre-line;
}

a.contacts-value:hover {
  text-decoration: underline;
}

.contacts-qr {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: calc(9 * var(--u));
  padding-bottom: calc(95 * var(--u));
  font-size: max(calc(45.93 * var(--u)), 15px);
  text-decoration: none;
}

.contacts-qr-frame {
  position: relative;
  width: calc(338 * var(--u));
  aspect-ratio: 338 / 351;
}

.contacts-qr-border {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.contacts-qr-code {
  position: absolute;
  left: 5%;
  top: 4.8%;
  width: 90%;
  height: 82%;
  border-radius: calc(32 * var(--u));
}

@media (max-width: 1199px) {
  .contacts-logo {
    width: min(56vw, 440px);
  }

  .contacts-list {
    gap: 20px;
    padding-bottom: 0;
  }

  .contacts-label {
    margin-bottom: 6px;
  }

  .contacts-qr {
    gap: 8px;
    padding-bottom: 0;
  }

  .contacts-qr-frame {
    width: 140px;
  }

  .contacts-qr-code {
    border-radius: 12px;
  }
}

@media (max-width: 767px) {
  .contacts {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto auto;
  }

  .contacts-logo {
    width: 72vw;
  }

  .contacts-qr {
    align-items: flex-start;
  }

  .contacts-qr-frame {
    width: 120px;
  }
}
</style>
