# design.md – UI Design System

This document defines the complete visual design language of AURA so the interface looks consistent and professional.

---

## 1. Color & Theme

### Primary Theme: Dark Mode (Default)

AURA uses a modern dark theme because it feels premium and reduces eye strain during long use.

### Color Palette

| Name                | Hex Code   | Usage                              |
|---------------------|------------|------------------------------------|
| Background          | `#0f0f0f`  | Main app background                |
| Surface             | `#1a1a1a`  | Cards, sidebar, chat area          |
| Surface Light       | `#262626`  | Hover states, input fields         |
| Primary (Accent)    | `#6366f1`  | Buttons, active states, highlights (Indigo) |
| Primary Hover       | `#4f46e5`  | Button hover                       |
| User Message        | `#6366f1`  | User chat bubble                   |
| Assistant Message   | `#262626`  | Assistant chat bubble              |
| Text Primary        | `#ffffff`  | Main text                          |
| Text Secondary      | `#a3a3a3`  | Secondary text, timestamps         |
| Success             | `#22c55e`  | Success status                     |
| Warning             | `#f59e0b`  | Thinking / warning                 |
| Error               | `#ef4444`  | Errors                             |
| Border              | `#333333`  | Subtle borders                     |

> **Implementation:** these colors are registered in `frontend/tailwind.config.js`
> under `colors.aura.*` (e.g. `bg-aura-surface`, `text-aura-text-secondary`).
> Always use the tokens, never raw hex in components.

### Status Colors

- **Listening** → Green (`#22c55e`)
- **Thinking** → Amber (`#f59e0b`)
- **Speaking** → Indigo (`#6366f1`)
- **Idle** → Gray

### Optional Light Theme
A light theme can be added later, but dark theme is the main focus.

---

## 2. Fonts

### Font Family

**Primary Font:** Inter (or system UI font)

```css
font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

**Why Inter?**
- Excellent readability
- Modern geometric look
- Works very well for dashboards and chat interfaces

### Fallback
If Inter is not loaded, the system default UI font should be used.

---

## 3. Typography

### Type Scale

| Element              | Size     | Weight    | Line Height | Usage                     |
|----------------------|----------|-----------|-------------|---------------------------|
| Page Title           | 24px     | 700       | 1.2         | "AURA" heading            |
| Section Title        | 18px     | 600       | 1.3         | Sidebar titles            |
| Body Text            | 15px     | 400       | 1.5         | Chat messages             |
| Small Text           | 13px     | 400       | 1.4         | Timestamps, status        |
| Button Text          | 14px     | 500       | 1           | All buttons               |
| Input Text           | 15px     | 400       | 1.4         | Text input                |

### Rules

- Keep line length comfortable in chat bubbles
- Use medium weight for important UI elements
- Avoid pure white text on pure black for long reading (use off-white)
- Maintain good contrast (WCAG AA minimum)

---

## 4. UI Components Style Guide

### Chat Bubbles
- User messages → Right aligned, Indigo background, white text
- Assistant messages → Left aligned, dark surface, white text
- Rounded corners (12px – 16px) → `rounded-2xl`
- Maximum width ≈ 75% → `max-w-[75%]`

### Microphone Button
- Large circular button
- Primary color when idle
- Pulsing animation when listening
- Clear visual feedback

### Input Box
- Rounded (`rounded-2xl`)
- Dark surface background
- Subtle border (`border-aura-border`)
- Focus ring in primary color → `focus-within:border-aura-primary`

### Sidebar
- Darker than main area
- Clean icons + labels
- Clear separation from chat area (right border `border-aura-border`)

### Spacing
- Use consistent spacing scale (4px, 8px, 12px, 16px, 24px, 32px)
- Prefer generous padding inside cards and bubbles

---

## 5. Component States

Every interactive component should define these states:

| State | Rule |
|-------|------|
| Default | Normal colors, readable text |
| Hover | Lighten surface (`bg-aura-surface-light`) or `hover:bg-aura-primary-hover` for primary buttons |
| Focus | Visible focus ring in primary color (keyboard accessibility) |
| Disabled | 40% opacity, `cursor-not-allowed`, no hover effect |
| Active/Selected | Primary color accent (e.g. indigo dot in sidebar nav) |
| Error | Red (`#ef4444`) message text or border |
| Loading | Spinner or "Thinking..." text; button disabled while pending |

---

## 6. Visual Principles

1. **Clarity first** – User should instantly understand the status
2. **Minimal distraction** – Clean interface, no unnecessary elements
3. **Strong hierarchy** – Important actions stand out
4. **Smooth feedback** – Every action should have visual response
5. **Premium feel** – Dark theme + good typography + proper spacing

---

## 7. Motion & Feedback

- Transitions: 150–200 ms ease for hover/focus (`transition-colors`)
- Status changes: soft color cross-fade, no jarring jumps
- Listening mic: pulsing ring animation (`animate-pulse` acceptable, custom preferred)
- Message appear: subtle fade/slide-in (200–300 ms)
- Avoid excessive animation — motion should communicate, not distract

---

## 8. Layout & Responsiveness

- Desktop-first, minimum comfortable width ≈ 1024px
- Sidebar fixed at 256px (`w-64`), collapses later if needed
- Chat area uses flexible column layout (header / messages / input)
- Input bar stays pinned to the bottom of the chat area
- On small screens: sidebar may hide behind a toggle (future work)

---

## 9. Accessibility

- All interactive elements are real buttons/inputs (not divs with onClick)
- Every icon button has an `aria-label`
- Focus states are visible
- Text contrast meets WCAG AA minimum
- Status is communicated with text too, not color alone (e.g. "Thinking..." label)

---

## 10. Implementation Notes (Tailwind)

Recommended Tailwind classes examples:

- **No emojis in the UI** — all iconography uses inline SVG icons or text labels (emojis allowed only in terminal/chat communication)
- Background: `bg-neutral-950` → use `bg-aura-bg`
- Surface: `bg-neutral-900` → use `bg-aura-surface`
- Primary button: `bg-indigo-500 hover:bg-indigo-600` → use `bg-aura-primary hover:bg-aura-primary-hover`
- Text: `text-white` / `text-neutral-400` → use `text-white` / `text-aura-text-secondary`
- Rounded: `rounded-2xl`
- Shadow: `shadow-lg`

---

## Version

**v1.1** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added component state spec, motion guidance, layout/responsiveness notes, accessibility checklist. |
| v1.1 | 2026-08-16 | Added no-emoji-in-UI rule (SVG icons instead). |

---

**Follow this design system strictly so the final UI looks consistent and professional.**
