# Product Scene Generator (Frontend)

A modern, responsive frontend for an AI Product Scene Generator, built with Next.js 15 (App Router), TypeScript, Tailwind CSS, and React. This is a **frontend-only** demo — all generation is mocked in `services/api.ts`.

## Getting started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Project structure

```
app/
  layout.tsx          Root layout, global styles
  page.tsx             Main page — owns all app state, composes components
  globals.css          Tailwind + base styles

components/
  Upload.tsx            Drag-and-drop / click-to-browse image uploader with preview
  ScenarioSelector.tsx   Grid of 10 selectable marketing scenario cards
  GenerateButton.tsx     Primary CTA with normal/loading states
  Progress.tsx           Animated progress bar shown during generation
  Gallery.tsx             Responsive grid of generated images

services/
  api.ts                Mocked API layer — swap for real fetch() calls later

types/
  index.ts               Shared TypeScript interfaces
```

## Connecting a real backend later

Everything backend-related is isolated in `services/api.ts`. To wire up a real
FastAPI backend:

1. Replace the body of `generateSceneImages` with a `fetch("/api/generate", { method: "POST", body: formData })` call (or a call to your FastAPI URL).
2. Keep the function signature (`payload`, `onProgress`) the same, or adapt `app/page.tsx` accordingly — for example switching from simulated per-image progress to real progress via polling, SSE, or WebSockets.
3. Enable the disabled "Download" button in `Gallery.tsx` once real image URLs are returned.

No other component needs to change, since `app/page.tsx` is the only place that calls the API service.

## Notes

- State (`image`, `preview`, `selectedScenarios`, `loading`, `progress`, `generatedImages`) is lifted into `app/page.tsx` and passed down via props — no external state library.
- Generated images use [picsum.photos](https://picsum.photos) placeholders, seeded per scenario ID for consistent placeholders during a session.
- Styling uses Tailwind CSS only — no external UI component libraries.
