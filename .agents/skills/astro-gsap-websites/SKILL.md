---
name: astro-gsap-websites
description: Guía paso a paso para construir sitios web con animaciones de desplazamiento (scroll) interactivas usando Astro y GSAP.
metadata:
  tags: astro, gsap, scrolltrigger, websites, ui, animation, step-by-step
---

## Cuándo usar esto

Usa esta guía cuando necesites crear o configurar proyectos para sitios web de productos animados, interactivos, de alto rendimiento y listos para producción, mediante animaciones de desplazamiento (scroll), utilizando Astro, GSAP y videos generados con IA.

## Flujo de Trabajo y Metodología

Esta es una guía paso a paso basada en la metodología para construir sitios web con animaciones de desplazamiento (scroll) interactivas, optimizados para SEO y listos para producción.

### 1. El Stack Tecnológico
Para que un sitio no solo sea "bonito" sino también funcional y vendible, utilizaremos:
- **Framework:** Astro (ideal para rendimiento y fundamentos de SEO).
- **IA de Construcción:** Claude Code (vía terminal para agilizar el desarrollo).
- **Diseño de UI:** Google Stitch (para evitar el "look" genérico de IA).
- **Generación de Imágenes:** Google AI Studio (Modelo: Nano Banana Pro).
- **Generación de Video:** fal.ai (usando modelos como Seed Dance o Cling 3.5).
- **Animación:** GSAP (GreenSock Animation Platform) para controlar el desplazamiento total.

### 2. Generación de Activos Visuales
El "efecto wow" de esta guía se basa en un producto que se "desarma" mientras el usuario hace scroll.
- **Imagen del Producto Final:** En Google AI Studio, genera una imagen de alta calidad de un producto (ej. un micrófono de lujo). Incluye en los detalles rápidos de la cámara y la distancia focal para mantener la consistencia.
- **Imagen Desensamblada:** Usa la primera imagen como referencia y pide al modelo que cree el mismo producto pero con sus componentes internos flotando (desarmados). Asegúrese de que los elementos se expandan hacia los lados para dar profundidad.
- **Video de Transición:** Sube ambas imágenes a fal.ai.
  - *Inicio:* Imagen del producto armado.
  - *Fin:* Imagen del producto desarmado.
  - *Indicación:* "Anima el proceso de desmontaje del producto para que sus componentes queden flotantes. Haz que sea un proceso suave y lujoso."

### 3. Diseño de la interfaz con Google Stitch
Para que el sitio no parezca una plantilla básica, usa Google Stitch:
- Sube la imagen del producto terminado.
- Pide una página de inicio moderna y de alta tecnología.
- *Consejo de personalización:* Define una paleta de colores y añade un color "fuerte" o neón para los CTA (Call to Action) para que resalten sobre el diseño minimalista.
- Descarga el archivo .zip con los elementos de diseño.

### 4. Desarrollo con Claude Code
Una vez tengas el video y el diseño, es hora de programar.
- **Preparación:** Abre tu editor de código (como Cursor o VS Code) en la carpeta del proyecto.
- **Ejecución de Claude:** Inicia Claude Code en la terminal.
- **El Prompt Maestro:** Dale a Claude las instrucciones del sitio, adjunta el video, el diseño de Stitch y la descripción de la marca. Indica que utiliza Astro y GSAP.
- Claude se encargará de extraer los fotogramas del vídeo (pueden ser ~120 imágenes) y optimizarlos en formato .webp. Configurará el scaffolding de Astro y la lógica de animación donde el scroll controla el progreso del video deconstruido.

### 5. Optimización SEO (El toque profesional)
Un sitio animado no sirve de nada si no posiciona. Pide a Claude Code lo siguiente:
- **Datos estructurados (Schema):** Implementa Product Schema, Offer y Organization en JSON-LD. Esto ayuda a los motores de búsqueda de IA a entender qué vendes.
- **Palabras clave LSI:** No te limites a la palabra clave principal. Agregue términos relacionados semánticamente en los encabezados y textos.
- **Meta Tags:** Optimiza el title tag y la meta description para que sean atractivos y contengan la palabra clave principal.

### 6. Despliegue y Auditoría
Antes de entregar al cliente, el sitio debe ser rápido y responsivo.
- **Puesta en escena:** Usa Claude Code para subir el sitio a Cloudflare Pages usando Wrangler.
- **Prueba de Velocidad:** Pasa la URL por GTMetrix o Google Page Speed Insights.
  - *Regla de oro:* Si carga en más de 3 segundos, optimiza las fuentes y el peso de los marcos de imagen.
- **Mobile Check:** Verifica que la animación de GSAP sea fluida en dispositivos móviles y que el menú no estorbe la experiencia visual.

### Resumen de Flujo de Trabajo
| Fase | Herramienta Principal | Resultado |
| :--- | :--- | :--- |
| Concepto | Google AI Studio | Imágenes del producto |
| Movimiento | fal.ai | Video de deconstrucción |
| Diseño UI | Google Stitch | Guías de marca y layout |
| Construir | Claude Code + Astro | Código fuente optimizado |
| SEO | JSON-LD + LSI | Visibilidad en buscadores |
| Lanzamiento | Cloudflare | Sitio web en vivo (Staging) |

---

## El Prompt Maestro

```text
THE PROMPT (copy everything below)
========================================

I have a product video and a design system file. Build me a scroll-animated product website using Astro and GSAP ScrollTrigger.

I am providing you with three things directly in this chat:
1. The finished product MP4 video: [drag your MP4 file into the chat]
2. The brand design system: [drag your DESIGN.md / Stitch export into the chat]
3. Product information: [paste brand name, product name, tagline, specs, price, description, and any other copy you want on the site]

You do not need to generate any images or video yourself. All creative assets are already provided above.

REFERENCE REPOS / DOCS (use these for correct APIs and install commands):
- Astro: https://github.com/withastro/astro  (docs: https://docs.astro.build)
- GSAP: https://github.com/greensock/GSAP  (docs: https://gsap.com/docs/v3/)
- GSAP ScrollTrigger: https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- FFmpeg: https://github.com/FFmpeg/FFmpeg  (docs: https://ffmpeg.org/documentation.html)
- Wrangler (Cloudflare deploy): https://github.com/cloudflare/workers-sdk

STEP 0 — DEPENDENCY CHECK (do this FIRST, before anything else):

Run these checks and report what is missing. For anything missing, install it automatically for my platform (detect macOS vs Linux vs Windows) and confirm the install succeeded before moving on. Do NOT skip any check.

1. Node.js 18+:    node --version
   - If missing on macOS:  brew install node
   - If missing on Linux:  use nvm (https://github.com/nvm-sh/nvm) to install node 20
2. npm:             npm --version  (ships with Node)
3. FFmpeg:          ffmpeg -version
   - macOS:   brew install ffmpeg
   - Linux:   sudo apt-get install -y ffmpeg
   - Windows: winget install Gyan.FFmpeg
4. Wrangler CLI (for Cloudflare Pages deploy, optional but preferred):
                    wrangler --version
   - Install:  npm install -g wrangler
5. Homebrew (macOS only, required above):  brew --version
   - Install: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
6. API keys / env vars (optional, only for deploy):
   - CLOUDFLARE_API_TOKEN (optional, only needed if you auto-deploy to Cloudflare Pages via wrangler at the end). You do NOT need any image or video generation API keys, because I am providing the finished MP4 video, the design system markdown, and the product information directly in this chat.
   Check with: echo $CLOUDFLARE_API_TOKEN. If empty and I ask for a deploy, stop and ask me to paste it, do not hardcode it, write it to a local .env that is gitignored.

After each install, re-run the version check to verify it worked. If any install fails, STOP and tell me exactly which dependency failed and why, do not try to work around it.

Project-level npm packages you will install via npm install inside the Astro project (not global):
- astro           → https://www.npmjs.com/package/astro
- gsap            → https://www.npmjs.com/package/gsap  (includes ScrollTrigger)

What I need you to do AFTER the dependency check passes:

1. Extract the video into WebP frames using FFmpeg (24fps, quality 85)
2. Scaffold an Astro project (npm create astro@latest) and install GSAP (npm install gsap)
3. Copy the extracted frames into the project public/frames/ directory
4. Use the design system markdown to set all colors, typography, spacing, and component styles
5. Build the following page sections:

   HERO SECTION (scroll frame animation):
   - Full-viewport canvas element
   - GSAP ScrollTrigger scrubs through the WebP frames as user scrolls
   - Pin the hero section so it stays fixed while frames play
   - Overlay the brand name with a neon glow effect
   - Add small "technical overlay" labels in the corners for aesthetic
   - Text animations: the hero text should enter with a staggered slide-up on page load, then exit with each line flying in different directions (left, scale-up, right) as user scrolls
   - Mid-scroll: show a secondary tagline that fades in and out over the frames
   - End of scroll: show product details (name, specs) on either side of the final frame before unpinning

   NAVIGATION:
   - Glassmorphic fixed nav with brand logo and links
   - Nav hides on scroll down, reappears on scroll up

   FEATURES SECTION:
   - Cards with product specs, scroll-triggered staggered reveal
   - Animated progress bars inside each card
   - Mouse-following neon glow hover effect on cards using brand colors
   - A large statement/quote with letter-by-letter scramble reveal animation
   - Animated counting stats strip

   CTA SECTION:
   - Gradient headline using brand colors
   - Ambient glow background effect
   - Scroll-triggered fade-in

6. Use a single GSAP master timeline for the hero to avoid ScrollTrigger pin conflicts
7. Run the dev server so I can preview it

Make the website feel premium, immersive, and heavily animated. Every section should have scroll-triggered entrance animations.
========================================
END OF PROMPT
========================================
```
