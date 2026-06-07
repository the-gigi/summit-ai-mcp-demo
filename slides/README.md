# Slides — Custom MCP Server Architecture for Personal AI Assistance

[Slidev](https://sli.dev) deck for the talk. Source is [`slides.md`](slides.md);
the agenda + time budgets live in [`AGENDA.md`](AGENDA.md).

## Run

```bash
cd slides
npm install            # see note below if your npm registry rejects scoped packages
npm run dev            # live preview at http://localhost:3030 (press `p` for presenter mode)
```

> **npm registry note:** if `npm install` 400s on scoped packages (e.g. behind a
> proxy that mishandles `@slidev/...`), install against the public registry:
> `npm install --registry=https://registry.npmjs.org`

## Export

```bash
npm run build          # static site → dist/
npm run export         # PDF (needs playwright-chromium: npx playwright install chromium)
```

## Presenting

- `npm run dev`, then `p` for presenter mode (notes are in `<!-- ... -->` comments).
- Code slides use Slidev line-highlighting (`{1|2-3}`) to reveal code step by step.
- Arrow keys / space to advance; `o` for slide overview.
