// Pre-render art compositions with huge blurs (glows) to WebP with headless Chrome.
// Mobile GPUs approximate such blurs differently, which changes colours; an image looks the same everywhere.
// Usage: node scripts/figma/raster.mjs   (CHROME_PATH overrides the Chrome binary)
import fs from 'node:fs'
import path from 'node:path'
import puppeteer from 'puppeteer-core'
import sharp from 'sharp'

const root = path.join(import.meta.dirname, '../..')
const cache = path.join(import.meta.dirname, '.cache')
const names = JSON.parse(fs.readFileSync(`${root}/src/figma/raster.json`))
const chrome = process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

const css = fs.readFileSync(`${root}/src/style.css`, 'utf8').match(/\.fg-svg \{[^}]*\}/)[0]
const html = (node) =>
  `<div style="${node.s.replace(/"/g, '&quot;')}"${node.cl ? ` class="${node.cl}"` : ''}>${node.h ?? ''}${(node.c ?? []).map(html).join('')}</div>`

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--allow-file-access-from-files'] })
fs.mkdirSync(`${root}/public/figma/art`, { recursive: true })
for (const name of names) {
  const art = JSON.parse(fs.readFileSync(`${root}/src/figma/art/${name}.json`))
  const file = `${cache}/raster-${name}.html`
  const body = html(art.root).replaceAll('/figma/', `file://${root}/public/figma/`)
  fs.writeFileSync(file, `<!doctype html><style>body{margin:0;background:#000}${css}</style>${body}`)
  const page = await browser.newPage()
  await page.setViewport({ width: Math.ceil(art.w), height: Math.ceil(art.h), deviceScaleFactor: 1 })
  await page.goto(`file://${file}`, { waitUntil: 'networkidle0' })
  await new Promise((r) => setTimeout(r, 500))
  const png = await page.screenshot({ type: 'png', omitBackground: false })
  await sharp(png).webp({ quality: 90 }).toFile(`${root}/public/figma/art/${name}.webp`)
  await page.close()
}
await browser.close()
