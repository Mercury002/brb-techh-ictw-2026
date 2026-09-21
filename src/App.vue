<!-- @format -->

<script setup lang="ts">
import LangSwitcher from "./components/LangSwitcher.vue";
import AboutSection from "./sections/AboutSection.vue";
import ContactsSection from "./sections/ContactsSection.vue";
import CoverSection from "./sections/CoverSection.vue";
import DirectionSection from "./sections/DirectionSection.vue";
import DirectionsSection from "./sections/DirectionsSection.vue";
import PartnersSection from "./sections/PartnersSection.vue";
import ServicesSection from "./sections/ServicesSection.vue";
</script>

<template>
  <LangSwitcher />
  <main>
    <CoverSection />
    <AboutSection />
    <ServicesSection />
    <DirectionsSection />
    <DirectionSection id="fintech" layout="grid" :icons="['computer-phone-sync', 'credit-card-change', 'money-receive-02', 'api', 'img:feature-superapp', 'img:feature-biometric']" :visual="{ art: 'fintech-visual', x: 1951, y: 235, w: 1449 }" />
    <DirectionSection id="education" layout="row" :icons="['mentoring', 'online-learning-02', 'computer-video-call', 'certificate-02', 'img:feature-internship']" :visual="{ art: 'education-visual', x: 1924, y: 756, w: 1459 }" />
    <DirectionSection id="ai" layout="grid" :icons="['ai-voice-01', 'chat-bot', 'artificial-intelligence-04', 'ai-content-generator-02', 'ai-computer', 'ai-programming']" :visual="{ img: 'ai-visual', x: 1770, y: 573, w: 1500 }" />
    <DirectionSection id="outsourcing" layout="row" :icons="['user-add-01', 'user-group-02', 'user-round-key', 'inspect-code', 'analytics-up']" :visual="{ img: 'outsourcing-visual', x: 1827, y: 429, w: 1475 }" />
    <DirectionSection id="b2b" layout="grid" :icons="['notebook', 'login-method', 'api', 'dashboard-square-setting', 'rocket-01']" :visual="{ img: 'b2b-visual', x: 1783, y: 813, w: 1536 }" />
    <DirectionSection id="bank" layout="grid" :icons="['user-group-03', 'search-dollar', 'brochure', 'chart-down', 'dashboard-square-01']" :visual="{ art: 'bank-visual', x: 2035, y: 586, w: 1473 }" />
    <PartnersSection />
    <ContactsSection />
  </main>
</template>
<style>
.nl-wrap {
  display: none;
  visibility: hidden;
  opacity: none;
}
</style>
