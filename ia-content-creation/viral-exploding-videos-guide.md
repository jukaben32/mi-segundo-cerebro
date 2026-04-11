# 🌋 Guía: Cómo Crear Videos Virales "Explosivos" (Gratis)

Esta guía documenta la estrategia para generar anuncios cinemáticos de alto impacto (estilo "Reveal" explosivo), donde un objeto base estalla y su energía o partes construyen una habitación entera. Es excelente para revelaciones de productos (Ej. Zapatos, Consolas, Gafas VR).

## 1. La Arquitectura del Prompt (Estructura JSON)

Para que modelos de video consistentes (como **Veo 3**) puedan digerir una transformación tan dramática sin perder coherencia, no le hablamos en prosa, le hablamos en **JSON**. 

Esta es la estructura maestra. Puedes inyectar esto en Veo3 (o en un bot de n8n) para obtener un resultado demencial:

```json
{
  "globals": {
    "style": "photorealistic cinematic, high-contrast, dramatic",
    "aspect_ratio": "9:16",
    "mood": "bold, high-energy, premium",
    "color_palette": "deep blacks, electric blues, stark whites"
  },
  "parameters": {
    "brand": "Nike",
    "logo": "white swoosh",
    "room_type": "minimalist concrete vault",
    "featured_product": "Air Jordan 1s"
  },
  "sequence": [
    {
      "scene": 1,
      "duration_seconds": 3,
      "description": "An empty, dark room is revealed. A single box sits in the center.",
      "camera": {
        "angle": "wide, eye-level, symmetrical",
        "movement": "slow dolly push-in"
      },
      "lighting": "A single soft spotlight from above illuminates the box, leaving the corners of the room in shadow.",
      "elements": [
        {
          "name": "room",
          "description": "An empty {{room_type}} with dark wood floors."
        },
        {
          "name": "shoebox",
          "description": "A matte black {{brand}} shoebox with a {{logo}} sits perfectly centered."
        }
      ],
      "audio": "low, deep ambient hum, subtle suspenseful synth pad"
    },
    {
      "scene": 2,
      "duration_seconds": 2,
      "description": "The box violently bursts open. Light and energy emanate from within.",
      "camera": {
        "angle": "same as scene 1",
        "movement": "quick shake, rapid zoom into the exploding box"
      },
      "lighting": "Intense, cool blue light erupts from the box, casting dynamic shadows.",
      "actions": [
        {
          "element": "shoebox",
          "action": "The lid and sides fly apart explosively."
        }
      ],
      "audio": "Sudden bass drop (BOOM), whoosh sound effect, crackling energy."
    },
    {
      "scene": 3,
      "duration_seconds": 4,
      "description": "Objects and structures fly out of the light and assemble the final room.",
      "camera": {
        "angle": "wide",
        "movement": "pulls back to reveal the full room transformation"
      },
      "lighting": "The room is now lit by neon lights and spotlights, glowing with cool energy.",
      "actions": [
        {
          "element": "display_shelves",
          "description": "Floating shelves holding pairs of {{featured_product}} fly from the center and affix to the walls."
        },
        {
          "element": "neon_sign",
          "description": "A neon {{brand}} wall light materializes and flickers on."
        },
        {
          "element": "posters",
          "description": "Holographic posters of athletes flicker into existence on the back wall."
        }
      ],
      "audio": "High-tech assembly sounds, mechanical clicks, electrical hum, upbeat electronic music begins to build."
    },
    {
      "scene": 4,
      "duration_seconds": 3,
      "description": "The final, fully assembled sneaker vault is revealed in a dramatic hero shot.",
      "camera": {
        "angle": "low angle, wide",
        "movement": "static, epic hero shot"
      },
      "lighting": "Crisp, cool showroom lighting. Spotlights highlight the shoes.",
      "elements": [
        {
          "name": "final_room",
          "description": "A high-tech {{brand}} sneaker vault, perfectly assembled and glowing."
        }
      ],
      "audio": "Music hits its crescendo and holds, a final resonant synth note."
    }
  ]
}
```

## 2. Metodología de Uso

Existen dos vías para generar estos videos:

### A. Creación de un "GPT Generator" o n8n Bot:
En lugar de escribir tú este bloque gigante, debes darle a un GPT (o Claude) las instrucciones de escribir este YAML/JSON asegurando siempre que tenga una "escena pasiva, explosión central, re-ensamblaje y Hero Shot".

**Ejemplos de prompts básicos para que el GPT genere tu JSON:**
> "Make a video for the Nintendo Switch 2. The box is in a kid's boring bedroom. The box splits into its red and blue halves, and all the famous Nintendo characters and items fly out to build the ultimate Nintendo-themed game room."

> "Let's do a video for the new Apple Vision Pro. The headset itself is floating in an empty, dark, minimalist room. It completely disassembles and its parts build a holographic, interactive design studio of the future."

### B. El Método Gratuito (LMArena)
Si no deseas pagar la cuota corporativa de Veo 3:
1. Ve al Discord de **LMArena**.
2. Entra al canal `#video-arena` y pega tu estructura JSON.
3. El bot de Discord invocará dos modelos de IA ocultos (Generará dos videos a ciegas, como Veo3 y Sora o parecido).
4. Votas cuál es mejor y procedes a descargarlo a 1080p.
5. *Límite:* Puedes hacer esto hasta 8 veces cada 24 horas. (8 comerciales épicos diarios gratis con este método).

## 3. Combinación con Nano Banana (Pro-Tip)
Añádele todavía más control generando el "First Frame" en **Nano Banana**. Modifica tu caja (o producto) hasta que el cuarto oscuro luzca perfecto, y luego sube esa imagen + tu código JSON a la plataforma de video para obligarla a estallar tu propia creación. 
