import { ref, watchEffect } from 'vue'
import uz from './locales/uz.json'
import ru from './locales/ru.json'
import en from './locales/en.json'

export const LOCALES = ['uz', 'ru', 'en'] as const
export type Locale = (typeof LOCALES)[number]
export type Messages = typeof uz

const messages: Record<Locale, Messages> = { uz, ru, en }

const STORAGE_KEY = 'locale'

function initialLocale(): Locale {
  const fromUrl = new URLSearchParams(location.search).get('lang')
  let saved: string | null = null
  try {
    saved = localStorage.getItem(STORAGE_KEY)
  } catch {}
  const pick = fromUrl ?? saved
  return LOCALES.includes(pick as Locale) ? (pick as Locale) : 'uz'
}

export const locale = ref<Locale>(initialLocale())

watchEffect(() => {
  document.documentElement.lang = locale.value
  try {
    localStorage.setItem(STORAGE_KEY, locale.value)
  } catch {}
})

/** Texts of the current locale, e.g. `t().about.title`. */
export function t(): Messages {
  return messages[locale.value]
}
