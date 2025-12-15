# My Personal Map - Design System

## Color Palette

### Primary Colors

| Color | Hex | Usage | CSS Variable |
|-------|-----|-------|--------------|
| **Primary** | `#4F46E5` | Main brand color, primary actions, links | `--color-primary` |
| **Primary Light** | `#818CF8` | Hover states, light backgrounds | `--color-primary-light` |
| **Primary Dark** | `#3730A3` | Active states, dark accents | `--color-primary-dark` |
| **Secondary** | `#9333EA` | Secondary actions, badges | `--color-secondary` |
| **Accent** | `#F59E0B` | Call-to-action, highlights, markers | `--color-accent` |

### Semantic Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Success** | `#10B981` | Success messages, confirmations |
| **Warning** | `#F59E0B` | Warnings, important notices |
| **Error** | `#EF4444` | Errors, destructive actions |
| **Info** | `#06B6D4` | Information, tips |

### Neutral Scale (Light Mode)

| Shade | Hex | Usage |
|-------|-----|-------|
| **Gray 50** | `#F9FAFB` | Page background |
| **Gray 100** | `#F3F4F6` | Card background |
| **Gray 200** | `#E5E7EB` | Borders, dividers |
| **Gray 300** | `#D1D5DB` | Disabled elements |
| **Gray 400** | `#9CA3AF` | Placeholders |
| **Gray 500** | `#6B7280` | Secondary text |
| **Gray 600** | `#4B5563` | Body text |
| **Gray 700** | `#374151` | Headings |
| **Gray 800** | `#1F2937` | Strong emphasis |
| **Gray 900** | `#111827` | Primary text |

### Neutral Scale (Dark Mode)

| Shade | Hex | Usage |
|-------|-----|-------|
| **Dark 900** | `#0F172A` | Page background |
| **Dark 800** | `#1E293B` | Card background |
| **Dark 700** | `#334155` | Borders, dividers |
| **Dark 600** | `#475569` | Disabled elements |
| **Dark 500** | `#64748B` | Placeholders |
| **Dark 400** | `#94A3B8` | Secondary text |
| **Dark 300** | `#CBD5E1` | Body text |
| **Dark 200** | `#E2E8F0` | Headings |
| **Dark 100** | `#F1F5F9` | Strong emphasis |

## Typography

### Font Families

```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### Type Scale

| Size | Rem | Pixels | Usage |
|------|-----|--------|-------|
| **xs** | 0.75rem | 12px | Captions, labels |
| **sm** | 0.875rem | 14px | Small text, secondary info |
| **base** | 1rem | 16px | Body text |
| **lg** | 1.125rem | 18px | Emphasized text |
| **xl** | 1.25rem | 20px | H4 headings |
| **2xl** | 1.5rem | 24px | H3 headings |
| **3xl** | 1.875rem | 30px | H2 headings |
| **4xl** | 2.25rem | 36px | H1 headings |
| **5xl** | 3rem | 48px | Display text |

### Font Weights

- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

## Spacing Scale

Based on 4px base unit:

| Token | Value | Pixels |
|-------|-------|--------|
| **xs** | 0.25rem | 4px |
| **sm** | 0.5rem | 8px |
| **md** | 1rem | 16px |
| **lg** | 1.5rem | 24px |
| **xl** | 2rem | 32px |
| **2xl** | 3rem | 48px |
| **3xl** | 4rem | 64px |
| **4xl** | 6rem | 96px |

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| **sm** | 0.25rem | Small elements, badges |
| **md** | 0.375rem | Buttons, inputs |
| **lg** | 0.5rem | Cards, modals |
| **xl** | 0.75rem | Large containers |
| **2xl** | 1rem | Feature cards |
| **full** | 9999px | Circular elements, pills |

## Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

## Component Patterns

### Buttons

**Primary Button**
- Background: `--color-primary`
- Text: White
- Hover: `--color-primary-dark`
- Shadow: `--shadow-sm`
- Border radius: `--radius-md`
- Padding: `0.5rem 1rem`

**Secondary Button**
- Background: Transparent
- Border: 1px solid `--color-primary`
- Text: `--color-primary`
- Hover: Light primary background

**Accent Button**
- Background: `--color-accent`
- Text: White
- Used for primary CTAs (e.g., "Add Marker")

### Cards

- Background: White (light) / Dark-800 (dark)
- Border: 1px solid Gray-200 (light) / Dark-700 (dark)
- Border radius: `--radius-lg`
- Shadow: `--shadow-md`
- Padding: `1.5rem`

### Inputs

- Border: 1px solid Gray-300 (light) / Dark-600 (dark)
- Border radius: `--radius-md`
- Padding: `0.5rem 0.75rem`
- Focus: Primary color ring

### Map Markers

- Default: `--color-accent` (#F59E0B)
- Selected: `--color-primary` (#4F46E5)
- Label-based: Use semantic colors or generate from label name

## Icons

Use **Lucide Icons** for consistency across web and desktop:
- Modern, clean design
- Available as SVG for web
- Can be embedded in CustomTkinter

Common icons:
- Map: `map-pin`
- Add: `plus-circle`
- Edit: `edit-2`
- Delete: `trash-2`
- Settings: `settings`
- User: `user`
- Search: `search`
- Filter: `filter`

## Layout

### Desktop GUI Layout (CustomTkinter)

- **Sidebar**: 280px width
  - Navigation menu
  - Quick actions
  - User info

- **Main Content**: Flexible width
  - Map view (primary)
  - List view (secondary)

- **Top Bar**: 64px height
  - App title
  - Search bar
  - User menu

## Animation

### Transitions

```css
--transition-fast: 150ms ease-in-out;
--transition-base: 250ms ease-in-out;
--transition-slow: 350ms ease-in-out;
```

### Common Animations

- **Hover**: Scale 1.02, transition-fast
- **Click**: Scale 0.98, transition-fast
- **Fade In**: Opacity 0 → 1, transition-base
- **Slide In**: TranslateY 20px → 0, transition-base

## Accessibility

### Contrast Ratios

All text meets WCAG 2.1 Level AA:
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum

### Focus States

- Visible focus ring: 2px solid Primary color
- Offset: 2px
- Never remove focus indicators

### Dark Mode

- Automatic based on system preference
- Manual toggle available
- Smooth transition between modes

## Implementation

### CustomTkinter Configuration (Desktop)

```python
# themes/mypersonalmap_theme.json
{
  "CTk": {
    "fg_color": ["#F9FAFB", "#0F172A"]
  },
  "CTkButton": {
    "fg_color": ["#4F46E5", "#4F46E5"],
    "hover_color": ["#3730A3", "#3730A3"],
    "border_color": ["#4F46E5", "#4F46E5"],
    "text_color": ["#FFFFFF", "#FFFFFF"]
  },
  "CTkFrame": {
    "fg_color": ["#FFFFFF", "#1E293B"],
    "border_color": ["#E5E7EB", "#334155"]
  }
}
```

## UI Components Library

### Desktop (CustomTkinter)

Components will be created in `pymypersonalmap/gui/components/`:
- `custom_button.py`
- `custom_card.py`
- `custom_input.py`
- `custom_modal.py`
- `custom_sidebar.py`
- `map_viewer.py`

## Design Principles

1. **Consistency**: Unified visual language across the application
2. **Clarity**: Clear hierarchy, obvious interactions
3. **Efficiency**: Minimal clicks to accomplish tasks
4. **Accessibility**: WCAG 2.1 AA compliant
5. **Delight**: Smooth animations, thoughtful micro-interactions

## Figma Resources

For detailed mockups and prototypes, see:
- `/design/mockups/` (to be created)
- Components library
- User flows
- Wireframes
