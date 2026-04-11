# Cinematic Sites Skill

This agent skill is an instruction manual for build cinematic responsive websites from scratch, following a 4-step automated pipeline.

---

## 🧭 GOAL
Transform a basic or existing website into a high-end, premium, and "cinematic" landing page using scroll-driven animations and modular components.

---

## 🛠 THE 4-STEP PIPELINE

### 1. Brand Analysis 🔍
**Goal**: Deeply understand the current brand to extract the "soul" of the company.
- **Input**: Website URL.
- **Action**: Use your `read_url_content` or `read_browser_page` tools to scrape the site.
- **Extract**: 
  - Industry, target audience, and brand voice.
  - Primary, secondary, and accent colors (HEX/HSL).
  - Typography styles (Google Fonts recommendations).
  - Headline, tagline, and overall narrative.
- **Output**: Create a **Brand Card** (stand-alone HTML/CSS) to present to the user for approval.

### 2. Scene Generation 🎬
**Goal**: Create the cinematic "hero" video that will drive the scroll experience.
- **Action**: Propose 3 high-quality hero animation concepts (e.g., "Steam rising from a bowl of ramen", "A watch exploding into components").
- **Tools**: 
  - Use `generate_image` for the initial keyframe.
  - (Optional) Use video-to-video or image-to-video models (like Kling 1.0/Wavespeed or Nano Banana 2) to animate.
- **Approval**: Show the keyframes and/or video to the user before continuing.

### 3. Website Build 🏗️
**Goal**: Assemble the final page using the 30 modular cinematic components.
- **Structure**:
  - **Hero**: Implement a scroll-scrubbed video component (map video frames to scroll position).
  - **Body**: Use components from the `cinematic-site-components` library:
    - `accordion-slider.html` for feature lists.
    - `sticky-stack.html` or `sticky-cards.html` for product stories.
    - `cursor-reactive.html` for environmental interactivity.
    - `text-mask.html` for dramatic headlines.
- **Aesthetics**: Premium, modern, dark mode by default unless brand dictates otherwise. Use Google Fonts (Inter, Outfit, etc.).

### 4. Deployment 🚀
**Goal**: Make the site live and shareable.
- **Action**: Deploy to Vercel.
- **Command**: `npx -y vercel --prod`.

---

## 🎨 DESIGN SYSTEM RULES
- **Visual Excellence**: Don't use basic colors. Use rich, balanced palettes.
- **Micro-Animations**: Add subtle hover effects and transitions.
- **Cinematic Feel**: The scrolling *must* feel like a movie, with the main product in the background or foreground changing state as the user scrolls.

---

## 📚 COMPONENT REFERENCE
The library at `c:\Users\hp\MisProyectos\cinematic-site-components` contains over 30 standalone modules. Use them as reference for Step 3.
- `index.html`: The visual hub of all modules.
- `accordion-slider.html`: Expanding image panels.
- `text-mask.html`: Headline fills on scroll.
- `glitch-effect.html`: Dramatic text entry.
- etc.
