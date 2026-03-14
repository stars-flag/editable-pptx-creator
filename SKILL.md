---
name: editable-pptx-creator
description: Generate fully editable PowerPoint presentations from ideas. Complete workflow: plan → generate HTML → export to editable PPTX. Creates native PowerPoint objects (not screenshots) so all text, shapes, colors, and layouts can be edited. Perfect for business presentations, reports, and any scenario requiring post-creation editing.
version: 1.0.0
metadata: {"openclaw":{"emoji":"📊","os":["darwin","linux","win32"],"homepage":"https://github.com/stars-flag/editable-pptx-creator","requires":{"bins":["python3"]},"install":[{"id":"python-pptx","kind":"uv","package":"python-pptx","label":"python-pptx (PPTX creation)"},{"id":"beautifulsoup4","kind":"uv","package":"beautifulsoup4","label":"BeautifulSoup4 (HTML parsing)"},{"id":"Pillow","kind":"uv","package":"Pillow","label":"Pillow (image processing)"}]}}
---

# Editable PPTX Creator

Generate fully editable PowerPoint presentations from raw ideas. This skill provides a complete workflow: from planning to HTML generation to editable PPTX export. Unlike screenshot-based approaches, this creates native PowerPoint objects that can be fully edited, modified, and integrated with the Office ecosystem.

## Core Philosophy

1. **Fully Editable Output** — Creates native PowerPoint objects (text boxes, shapes, colors) that can be edited in PowerPoint, not static screenshots.
2. **Complete Workflow** — Plan → Generate HTML → Export to PPTX. Each step can be executed independently or as a complete pipeline.
3. **Style Discovery** — Inherited from slide-creator: generate visual previews and let users choose from presets or custom styles.
4. **Theme System** — Multiple pre-built themes (Spring, Business, Creative, Minimal) with full customization support.
5. **Office Integration** — Output works seamlessly with PowerPoint, supports printing, PDF export, and all Office features.

## Command Flags

Parse the invocation to determine mode:

- **`--plan [prompt]`** — Planning mode. Create `PLANNING.md` with slide outline. **Stop — do NOT generate HTML.**
- **`--generate [instructions]`** — Generation mode. Read `PLANNING.md` if present, then generate HTML presentation.
- **`--export pptx [--theme THEME]`** — Export HTML to editable PPTX. Uses native PowerPoint objects.
- **`--list-themes`** — List all available themes.
- **`--verify <pptx_file>`** — Verify PPTX editability (count text boxes, shapes, check for screenshots).
- **No flag** — Auto-detect mode (Phase 0).

---

## Planning Mode (`--plan`)

Inherited from slide-creator. Creates a detailed outline for the presentation.

1. Scan `resources/` folder — read text/markdown files, note images.
2. Extract: topic, audience, tone, language, slide count, goals from the prompt.
3. Draft the plan following [references/planning-template.md](references/planning-template.md).
4. Save as `PLANNING.md` in the working directory.
5. Present slide count, structure, and key decisions. Ask for approval.
6. **Stop. Do NOT generate HTML.**

---

## Generation Mode (`--generate`)

Inherited from slide-creator. Generates HTML presentation from plan or prompt.

1. Read `PLANNING.md` if present (skip Phase 1/2 questions).
2. Style Discovery: generate 3 visual previews or select from presets.
3. Generate HTML presentation with:
   - Responsive viewport fitting
   - CSS animations
   - Inline editing support
   - Semantic HTML structure
4. Open in browser for preview.
5. **Stop. Do NOT export to PPTX.**

---

## Export Mode (`--export pptx`)

**Core feature of this skill.** Converts HTML to fully editable PPTX.

1. Find `*.html` in current directory (prefer most recently modified).
2. Parse HTML structure using BeautifulSoup:
   - Extract slide sections
   - Identify content types (title, lists, cards, poems, images)
   - Parse text, colors, and layout information
3. Apply selected theme (default: spring):
   - Load theme configuration from `themes/`
   - Map HTML colors to PPTX RGB values
   - Apply fonts and spacing
4. Build PPTX using python-pptx:
   - Create native PowerPoint objects
   - Text boxes for all text content
   - Shapes for backgrounds and decorations
   - Preserve layout and hierarchy
5. Verify editability:
   - Count text boxes and shapes
   - Ensure no screenshot objects
   - Validate all elements are editable
6. Save and report:
   - Output file path
   - Slide count
   - Editability statistics

**Theme options:**
- `spring` — Warm, vibrant spring theme (default)
- `business` — Professional, clean business theme
- `creative` — Bold, energetic creative theme
- `minimal` — Simple, elegant minimal theme

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A — New Presentation:** Check for `PLANNING.md` first. If it exists, read it and jump to Phase 3 (HTML generation).
- **Mode B — HTML to PPTX:** User has an `.html` file → go to Phase 4 (Export).
- **Mode C — Enhance Existing:** Read existing HTML, understand structure, then enhance or export.

---

## Phase 1: Content Discovery

Inherited from slide-creator. Gather presentation requirements.

1. Scan `resources/` folder for context.
2. Collect via single AskUserQuestion:
   - **Purpose** (single select): Pitch deck / Teaching+Tutorial / Conference talk / Internal presentation
   - **Length** (single select): Short 5-10 / Medium 10-20 / Long 20+
   - **Content** (single select): All content ready / Rough notes / Topic only
   - **Images** (single select): No images / ./assets / Other (user types path)
   - **Inline Editing** (single select): Yes / No
3. If user has content, ask them to share it.

---

## Phase 2: Style Discovery

Inherited from slide-creator. Visual style selection.

1. Ask via AskUserQuestion:
   - **"Show me options"** → generate 3 previews based on mood
   - **"I know what I want"** → show preset picker
2. Generate previews in `.claude-design/slide-previews/`
3. Present options and ask user to choose.

**Available Presets:**
- Bold Signal — Confident, high-impact
- Electric Studio — Clean, professional
- Creative Voltage — Energetic, retro-modern
- Dark Botanical — Elegant, sophisticated
- Notebook Tabs — Editorial, organized
- Pastel Geometry — Friendly, approachable
- Split Pastel — Playful, modern
- Vintage Editorial — Witty, personality-driven
- Neon Cyber — Futuristic, techy
- Terminal Green — Developer-focused
- Swiss Modern — Minimal, precise
- Paper & Ink — Literary, thoughtful

---

## Phase 3: Generate HTML

Inherited from slide-creator. Generate HTML presentation.

1. Read [references/html-template.md](references/html-template.md) for HTML structure.
2. Read [STYLE-DESC.md](references/STYLE-DESC.md) for viewport fitting and style details.
3. Generate HTML with:
   - Semantic structure
   - CSS variables for theming
   - Responsive design
   - Animations
   - Inline editing support
4. Open in browser for preview.

**Important:** Ensure HTML structure is compatible with PPTX export:
- Use semantic class names (`.slide`, `.title`, `.list-item`, `.card`, `.poem`)
- Include data attributes for content type hints
- Maintain consistent structure across slides

---

## Phase 4: Export to Editable PPTX

**Core feature.** Convert HTML to fully editable PPTX.

### HTML Parsing

Read [references/html-parsing-guide.md](references/html-parsing-guide.md) for detailed parsing rules.

**Supported HTML structures:**

```html
<!-- Title slide -->
<section class="slide">
  <h1>Main Title</h1>
  <p class="subtitle">Subtitle text</p>
</section>

<!-- Content slide with list -->
<section class="slide">
  <h2>Section Title</h2>
  <ul>
    <li class="list-item">Item 1</li>
    <li class="list-item">Item 2</li>
  </ul>
</section>

<!-- Card grid slide -->
<section class="slide">
  <h2>Card Grid</h2>
  <div class="card-grid">
    <div class="card">
      <h3>Card Title</h3>
      <p>Card content</p>
    </div>
  </div>
</section>

<!-- Poem slide -->
<section class="slide">
  <h2>Poems</h2>
  <div class="poem">
    <p class="poem-text">Poem text</p>
    <p class="poem-author">Author</p>
  </div>
</section>
```

### PPTX Building

Read [references/pptx-creation-guide.md](references/pptx-creation-guide.md) for PPTX creation patterns.

**Slide types supported:**

1. **Title Slide** — Main title + subtitle + decorations
2. **Content Slide** — Title + bullet list
3. **Card Grid Slide** — Title + 2x2 or 3x2 card grid
4. **Poem Slide** — Title + poem cards with author
5. **Image Slide** — Title + image with caption

**Key principles:**
- Use native PowerPoint shapes (text boxes, rectangles, ovals)
- Apply RGB colors from theme
- Use proper fonts (Microsoft YaHei for Chinese, Arial for English)
- Maintain aspect ratio (16:9 default)
- Add decorative elements (flowers, leaves, etc.)

### Theme Application

Themes are defined in `themes/*.json`:

```json
{
  "name": "Spring",
  "colors": {
    "primary": "#7CB342",
    "secondary": "#F48FB1",
    "accent": "#FFD54F",
    "text_primary": "#2E7D32",
    "text_secondary": "#5D4037",
    "bg_light": "#E8F5E9",
    "bg_pink": "#FCE4EC"
  },
  "fonts": {
    "heading": "微软雅黑",
    "body": "微软雅黑",
    "poem": "楷体"
  },
  "layout": {
    "slide_padding": 1.0,
    "content_gap": 0.5,
    "card_radius": 0.2
  }
}
```

### Verification

After generation, verify editability:

```python
{
  "text_boxes": 40,
  "shapes": 91,
  "images": 0,
  "screenshots": 0,
  "editable": true
}
```

---

## Phase 5: Delivery

1. **Clean up:** Delete `.claude-design/slide-previews/` if it exists.
2. **Generate speaker notes** if deck has 8+ slides:
   - Create `PRESENTATION_SCRIPT.md` with 2-4 sentences per slide.
3. **Open:** `open [filename].pptx` (or provide path).
4. **Summarize:**

```
Your editable PowerPoint presentation is ready!

📁 File: [filename].pptx
🎨 Theme: [Theme Name]
📊 Slides: [count]
✅ Editable: Yes (all text, shapes, and colors can be modified)

Editability Statistics:
  • Text boxes: [count]
  • Shapes: [count]
  • Images: [count]
  • Screenshots: 0 (fully editable)

To customize: Open in PowerPoint and edit any element directly.

To regenerate with different theme: run `editable-pptx-creator --export pptx --theme [theme]`
```

---

## Effect → Feeling Guide

| Feeling | Techniques |
|---------|-----------|
| Professional | Clean sans-serif fonts, minimal decoration, data-focused layouts |
| Warm & Friendly | Rounded corners, pastel colors, soft gradients, organic shapes |
| Bold & Confident | Strong contrast, large typography, vibrant accent colors |
| Elegant & Sophisticated | Serif fonts, muted palette, generous whitespace, subtle animations |
| Creative & Playful | Bright colors, varied layouts, decorative elements, bouncy animations |

---

## Example: Complete Workflow

1. **User:** "Create a presentation about AI in healthcare"
2. **Planning:** `--plan` → creates PLANNING.md with 8-slide outline
3. **Generation:** `--generate` → style discovery → generates HTML
4. **Preview:** HTML opens in browser, user reviews
5. **Export:** `--export pptx --theme business` → generates editable PPTX
6. **Delivery:** PPTX opens in PowerPoint, user can edit any element

---

## Example: HTML to PPTX Only

1. **User:** "Convert this HTML to editable PPTX" (provides presentation.html)
2. **Export:** `--export pptx --theme spring`
3. **Parsing:** HTML parsed, 8 slides detected
4. **Building:** PPTX generated with 91 shapes, 40 text boxes
5. **Verification:** All elements editable, no screenshots
6. **Delivery:** presentation.pptx ready for editing

---

## Related Skills

- **slide-creator** — For HTML-only presentations with advanced animations
- **frontend-design** — For interactive web pages beyond presentations

---

## Technical Details

### Dependencies

- **python-pptx** — PPTX file creation and manipulation
- **beautifulsoup4** — HTML parsing and content extraction
- **Pillow** — Image processing (optional, for image slides)

### File Structure

```
editable-pptx-creator/
├── SKILL.md                    # This file
├── README.md                   # User guide
├── references/                 # Reference documentation
│   ├── planning-template.md    # Planning template
│   ├── html-template.md        # HTML structure guide
│   ├── STYLE-DESC.md           # Style descriptions
│   ├── html-parsing-guide.md   # HTML parsing rules
│   └── pptx-creation-guide.md  # PPTX creation patterns
├── scripts/                    # Core scripts
│   ├── generate_html.py        # HTML generation
│   ├── generate_editable_pptx.py # Main PPTX generation
│   ├── html_parser.py          # HTML parsing module
│   ├── pptx_builder.py         # PPTX building module
│   └── theme_manager.py        # Theme management
└── themes/                     # Theme configurations
    ├── spring.json             # Spring theme
    ├── business.json           # Business theme
    ├── creative.json           # Creative theme
    └── minimal.json            # Minimal theme
```

### Key Differences from slide-creator

| Feature | slide-creator | editable-pptx-creator |
|---------|---------------|----------------------|
| Primary Output | HTML | Editable PPTX |
| PPTX Export | Screenshot-based | Native objects |
| Editability | No | Yes (fully editable) |
| Office Integration | No | Yes |
| HTML Generation | Yes | Yes (inherited) |
| Planning | Yes | Yes (inherited) |
| Style Discovery | Yes | Yes (inherited) |
| Theme System | Yes | Yes (extended) |

### When to Use This Skill

Use **editable-pptx-creator** when:
- You need to edit the presentation in PowerPoint
- You need to share with Office users
- You need to print or export to PDF
- You need to integrate with other Office documents
- You need a professional, business-ready format

Use **slide-creator** when:
- You only need web-based presentation
- You want advanced CSS animations
- You want inline editing in browser
- You don't need Office integration
