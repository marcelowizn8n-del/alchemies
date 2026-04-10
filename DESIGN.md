# Design System Specification: The Ethereal Canvas

## 1. Overview & Creative North Star

### The Creative North Star: "The Digital Alchemist"
This design system is not a utility; it is a premium stage for creation. Inspired by the cinematic depth of Midjourney and the fluid sophistication of RunwayML, the "Digital Alchemist" aesthetic treats the interface as a dark, infinite void where AI-generated content is the only source of light. 

To move beyond "standard" dark mode, we reject the rigid, boxed-in layouts of traditional SaaS. We embrace **intentional asymmetry**, **layered luminosity**, and **monolithic typography**. The goal is to make the user feel like they are operating a high-end physical console—one made of obsidian and light. We break the "template" look by using extreme white space and allowing elements to overlap, creating a sense of three-dimensional depth.

---

## 2. Colors: Tonal Depth & The "No-Line" Rule

Our palette is anchored in deep blacks and neutral grays, allowing the `primary` (Electric Violet) and `tertiary` (Soft Blue) accents to feel like bioluminescent energy.

### The "No-Line" Rule
**Explicit Instruction:** 1px solid borders are prohibited for sectioning. Structural boundaries must be defined solely through background color shifts or subtle tonal transitions. 
*   Instead of a border: Place a `surface-container-high` element over a `surface-dim` background. 
*   The transition is the boundary.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—stacked sheets of frosted glass.
*   **Base Layer:** `surface` (#0e0e0e) for the global canvas.
*   **Secondary Context:** `surface-container-low` (#131313) for sidebars or secondary navigation.
*   **Content Cards:** `surface-container-highest` (#262626) for active workspaces or primary focal points.
*   **Nesting:** Always move from darker to lighter as you move "closer" to the user.

### The "Glass & Gradient" Rule
Floating elements (modals, popovers, hovering toolbars) must utilize **Glassmorphism**.
*   **Fill:** `surface-variant` (#262626) at 60% opacity.
*   **Effect:** `backdrop-blur` (minimum 20px).
*   **Signature Texture:** Main CTAs should use a linear gradient from `primary` (#ba9eff) to `primary-dim` (#8455ef) at a 135° angle to give a sense of "liquid light."

---

## 3. Typography: The Editorial Voice

We use **Inter** (or Geist) as a high-performance, geometric sans-serif that balances technical precision with human readability.

*   **Display (The Statement):** Use `display-lg` (3.5rem) with tight letter-spacing (-0.02em). This is for "Hero" moments where the AI's power is introduced.
*   **Headlines (The Narrative):** `headline-md` (1.75rem) provides an authoritative, editorial feel. Use these sparingly to anchor large sections of content.
*   **Body (The Utility):** `body-md` (0.875rem) is the workhorse. High line-height (1.6) is mandatory to ensure the dark background doesn't "crush" the legibility.
*   **Labels (The Metadata):** `label-sm` (0.6875rem) in `on-surface-variant` (#adaaaa) should be uppercase with +0.05em tracking for technical details or prompt parameters.

---

## 4. Elevation & Depth: Tonal Layering

Shadows and borders are secondary to **color-based depth**.

### The Layering Principle
Achieve lift by stacking surface tiers.
*   **Example:** A generation settings panel should be `surface-container-low`. The individual input fields within it should be `surface-container-lowest` to create a "recessed" look, rather than an outlined one.

### Ambient Shadows
For floating elements that require a "Z-axis" lift:
*   **Color:** Use a tinted version of `on-primary` (#39008c) at 5% opacity.
*   **Blur:** Use extreme diffusion (e.g., `box-shadow: 0 20px 40px rgba(57, 0, 140, 0.05)`). It should feel like a soft glow, not a shadow.

### The "Ghost Border" Fallback
If accessibility requires a container boundary:
*   Use `outline-variant` (#494847) at **15% opacity**.
*   This creates a "whisper" of an edge that is only visible upon close inspection.

---

## 5. Components: Precision Utensils

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary-dim`), `on-primary` text, `xl` (0.75rem) roundedness.
*   **Secondary:** `surface-container-highest` background. No border. On-hover, shift background to `surface-bright`.
*   **Tertiary:** Transparent background, `primary` text. No box.

### Input Fields (The Prompt Box)
*   **Background:** `surface-container-lowest`.
*   **Shape:** `md` (0.375rem) roundedness.
*   **Focus State:** No thick border. Use a subtle 1px "Ghost Border" at 40% opacity of the `primary` color and a soft `primary_dim` outer glow.

### Cards & Lists
*   **Strict Rule:** No divider lines. Separate list items using 8px or 12px of vertical white space.
*   **Active State:** Use a `surface-bright` background shift and a 2px vertical "accent bar" of `tertiary` (#47c4ff) on the far left.

### Floating AI Toolbars
*   Use the **Glassmorphism** rule.
*   Corners must be `full` (pill-shaped) to contrast against the more architectural `md` corners of the main workspace.

---

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical layouts. Place your prompt bar off-center or allow images to bleed off the edge of the grid.
*   **Do** use "Breathing Room." If you think there is enough margin, double it.
*   **Do** use `tertiary` (#47c4ff) for "Success" or "AI Processing" states to differentiate from the `primary` violet branding.

### Don't
*   **Don't** use pure white (#ffffff) for long-form body text; use `secondary` (#e5e2e1) to reduce eye strain against the dark background.
*   **Don't** use 100% opaque borders. They "kill" the soul of a dark premium interface.
*   **Don't** use standard "Drop Shadows." If the element isn't glowing or blurring the background, it shouldn't be there.
*   **Don't** crowd the interface. If a feature isn't essential to the current generation step, hide it in a `surface-container` layer.