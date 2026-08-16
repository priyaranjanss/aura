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
| Page Title           | 24px     | 700       | 1.2         | “AURA” heading            |
| Section Title        | 18px     | 600       | 1.3         | Sidebar titles            |
| Body Text            | 15px     | 400       | 1.5         | Chat messages             |
| Small Text           | 13px     | 400       | 1.4         | Timestamps, status        |
| Button Text          | 14px     | 500       | 1            | All buttons               |
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
- Rounded corners (12px – 16px)
- Maximum width ≈ 75%

### Microphone Button
- Large circular button
- Primary color when idle
- Pulsing animation when listening
- Clear visual feedback

### Input Box
- Rounded
- Dark surface background
- Subtle border
- Focus ring in primary color

### Sidebar
- Darker than main area
- Clean icons + labels
- Clear separation from chat area

### Spacing
- Use consistent spacing scale (4px, 8px, 12px, 16px, 24px, 32px)
- Prefer generous padding inside cards and bubbles

---

## 5. Visual Principles

1. **Clarity first** – User should instantly understand the status
2. **Minimal distraction** – Clean interface, no unnecessary elements
3. **Strong hierarchy** – Important actions stand out
4. **Smooth feedback** – Every action should have visual response
5. **Premium feel** – Dark theme + good typography + proper spacing

---

## 6. Implementation Notes (Tailwind)

Recommended Tailwind classes examples:

- Background: `bg-neutral-950`
- Surface: `bg-neutral-900`
- Primary button: `bg-indigo-500 hover:bg-indigo-600`
- Text: `text-white` / `text-neutral-400`
- Rounded: `rounded-2xl`
- Shadow: `shadow-lg`

---

**Follow this design system strictly so the final UI looks consistent and professional.**
