// `dims`: record natural image sizes (needed by lib.py).
// default: write the images used by the page as WebP into public/figma:
//   public/figma/<ref>.webp       images inside art compositions (src/figma/art)
//   public/figma/img/<name>.webp  named images (src/figma/images.ts), cropped like in Figma
import sharp from 'sharp'
import fs from 'node:fs'
import path from 'node:path'

const cache = path.join(import.meta.dirname, '.cache')
const out = path.join(import.meta.dirname, '../../public/figma')
const ext = JSON.parse(fs.readFileSync(`${cache}/imgext.json`))
const read = (f) => JSON.parse(fs.readFileSync(`${cache}/${f}`))
const src = (ref) => `${cache}/imgs/${ref}.${ext[ref]}`

// display size in Figma px * 1.25 is enough for full-width desktop on retina screens
async function save(img, w, h, size, file) {
  const max = Math.max(w, h)
  const target = Math.min(max, Math.ceil(size * 1.25))
  if (target < max) img.resize(w >= h ? { width: Math.round((w * target) / max) } : { height: Math.round((h * target) / max) })
  await img.webp({ quality: 82, alphaQuality: 90 }).toFile(file)
}

if (process.argv[2] === 'dims') {
  const dims = {}
  for (const ref of Object.keys(ext)) {
    const m = await sharp(src(ref)).metadata()
    dims[ref] = [m.width, m.height, m.hasAlpha ? 1 : 0]
  }
  fs.writeFileSync(`${cache}/imgdims.json`, JSON.stringify(dims))
} else {
  const dims = read('imgdims.json')
  fs.rmSync(out, { recursive: true, force: true })
  fs.mkdirSync(`${out}/img`, { recursive: true })
  for (const [ref, size] of Object.entries(read('imgneed.json'))) {
    const [w, h] = dims[ref]
    await save(sharp(src(ref)), w, h, size, `${out}/${ref}.webp`)
  }
  for (const [name, { ref, crop, size }] of Object.entries(read('imgjobs.json'))) {
    let [w, h] = dims[ref]
    const img = sharp(src(ref))
    if (crop) {
      const [left, top, width, height] = crop
      img.extract({ left, top, width: Math.min(width, w - left), height: Math.min(height, h - top) })
      ;[w, h] = [width, height]
    }
    await save(img, w, h, size, `${out}/img/${name}.webp`)
  }
}
