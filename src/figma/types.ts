/** Node of a composition generated from the Figma file (scripts/figma/build.py). */
export interface SceneNode {
  /** inline css */
  s: string
  /** svg markup (fills, strokes, vector paths) */
  h?: string
  /** extra css class */
  cl?: string
  c?: SceneNode[]
}

export interface Art {
  /** size and position of the composition on its Figma page (px) */
  w: number
  h: number
  x: number
  y: number
  root: SceneNode
}
