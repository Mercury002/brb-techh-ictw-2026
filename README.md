# BRB-TECH landing

Vue 3 + Vite. One page with 12 sections (100vh each), built from the Figma file
`ENDaKLye6Xc08F7tOoGx26` (sections "Brochure uz / ru / en").

## Texts / translations

All texts live in `src/locales/{uz,ru,en}.json` with semantic keys (`about.title`, `fintech.features`…).
The language is switched in the top-right corner (also `?lang=ru`) and remembered in localStorage.

## Layout

`src/sections/*` — one component per page of the brochure, with responsive CSS:

- desktop (≥1200px): full width, sizes follow Figma via `--u` (1 Figma px = `100cqw / 3508`);
- tablet (768–1199px) and mobile (<768px): reflowed layouts with their own sizes (see `src/style.css`).

Assets extracted from Figma: `src/assets/icons/*.svg` (icons, logo), `public/figma/**` (images),
`src/figma/art/*.json` (decorative compositions — phone mockups, cover background — drawn by `FigmaArt.vue`).

Regenerate from Figma (overwrites locales, icons, images and art):

```sh
FIGMA_TOKEN=figd_... yarn figma
```
