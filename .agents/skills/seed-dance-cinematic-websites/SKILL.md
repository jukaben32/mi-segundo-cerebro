---
name: seed-dance-cinematic-websites
description: Workflow for building cinematic, high-converting websites using Claude Code and AI-generated looping video backgrounds (Seed Dance 2.0/Kling 3.0).
---

# Cinematic Websites Workflow with Claude Code & AI Video

This skill provides the exact step-by-step process for scaffolding cinematic, highly visual web applications and integrating AI-generated looping video assets. Follow these instructions when you are requested to build a "cinematic website", a "Seed Dance website", or a landing page with an AI looping video background.

## Step 1: Establish the Base Website Structure
The first goal is to scaffold a functioning, aesthetically pleasing website foundation. Avoid generic layouts—ensure maximum visual impact.

### Option A: Clone an Existing Template
1. Request the user to provide a visually impressive base repository link (e.g., a modern Astro, Next.js, or HTML/Vanilla CSS template).
2. Clone the provided repository into a fresh directory.
3. Completely restyle the color palette and copy according to the specific prompt/niche (e.g., "redesign the whole thing for a beautiful, premium coffee brand that's pink themed").

### Option B: Scaffold using Claude Code
1. Ask the user for:
   - Business niche (e.g., luxury car company).
   - Style preference (e.g., bold and dark, clean and modern).
   - Expected sections (e.g., Hero, Social Proof, Features, Footer).
2. Generate the base code focusing on modern web design practices (glassmorphism if appropriate, harmonious palettes, distinct typography).
3. If structural errors occur (e.g., black screens, missing dependencies), inspect the browser console and fix them immediately.

## Step 2: Generate Cinematic Videos
The "wow" factor of this process relies on creating a perfect, high-quality looping video background for the hero section using an AI video generator.

1. **Craft the Image Prompt**: Ask Claude (or do it yourself) to generate a detailed prompt for a stunning **static background image**. 
   *Example: "A beautiful bag of coffee beans, color scheme pink and black, gorgeous and cinematic. When we create a video, it will rotate on its axis."*
   *(If the user needs a brand logo incorporated, instruct them to add their logo file to the image generation process).*
2. **Generate the Image**: Instruct the user to run the prompt in an image generator (like **Midjourney**, **Higsfield**, or **Nano Banana**) to get a starting reference image.
3. **Craft the Animation Prompt**: Using the generated image, write a specific animation prompt focusing on continuous rotation or a subtle, seamless shift. 
   *Example: "The main object slowly spins on its axis, ending in the exact same position."*
4. **Generate the Video in a Dedicated AI Video Tool**:
   Advise the user to use **Kia.ai (Seed Dance 2.0)**, **Kling 3.0**, or **Higsfield**. Provide them with these specific configurations:
   - **Start & End Frame**: Use the exact SAME generated image for both the first frame and last frame to ensure a perfect loop.
   - **Resolution**: 720p or 2K.
   - **Aspect Ratio**: 16:9 (Landscape) or 1:1 (Square) depending on the UI layout.
   - **Duration**: ~7 seconds.

## Step 3: Integrate and Deploy
Once the user provides the generated MP4 video back to the workspace, seamlessly merge it with the UI.

1. **Integrate Video to Hero Section**:
   - Apply the video behind the main landing content as an `autoplay`, `loop`, `muted` background video.
   - Ensure you apply an overlay (e.g., a dark or tinted gradient/mask) on top of the video to create **sufficient contrast** so that the overlaid H1 tags and buttons remain sharply legible.
   - *Micro-optimization*: Ensure the video fades nicely into the solid background color of the subsequent sections (e.g., darkening the edges via CSS).
2. **Push to GitHub**:
   Initialize Git, commit the changes, and optionally use the GitHub CLI (`gh repo create`) to push the project to an active repository.
3. **Deploy**:
   Instruct the user to connect their GitHub to Vercel/Netlify for immediate public deployment.

---
**Core Requirement**: Flawless aesthetics and conversion-focused wireframes are the priority. Do not accept basic, boxy CSS layouts. The background video must loop seamlessly.
