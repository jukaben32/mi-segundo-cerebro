# 🖼️➡️🖼️ Guía: Frame to Frame (Video por Interpolación)

Esta guía documenta la técnica de **"First to Last Frame Generation"**, una de las corrientes más populares para crear transiciones de video dinámicas y controladas.

## ¿Qué es Frame to Frame?
En lugar de darle un único fotograma a la Inteligencia Artificial y dejar que adivine el desenlace, le entregas **la foto inicial** y **la foto final**. 
La manera en la que cambias la perspectiva, la ropa o el entorno entre ambas imágenes es lo que obliga a la IA a calcular o "dirigir" el movimiento de la cámara para unir esos dos puntos en el video.

## Paso 1: Creación de los Límites (Los Fotogramas)
Utiliza **Midjourney**, **ChatGPT** o tu máquina de **Nano Banana** para generar ambas imágenes. 
- *Ejemplo:* 
  - **Frame 1:** Un hombre viendo la pantalla de *SportGuru AI* en su celular.
  - **Frame 2:** El mismo hombre (usando Nano Banana para mantener la consistencia del personaje) pero ahora con una chaqueta más cara y celebrando, con un fondo de estadio.

## Paso 2: Motores de Video Duales
No todas las IAs soportan cargar dos imágenes. Las herramientas modernas que sí lo permiten y logran esta técnica de forma nativa (y que puedes usar gratis) son:
- **Hailuo AI** (Minimax) - `https://hailuoai.video/create/image-to-video`
- **Veo 3.1** (Google Labs) - `https://labs.google/flow/about`
- **Kling AI** (Kuaishou)

**La Receta Final:** Insertas el *First Frame*, el *Last Frame* y un Prompt escrito. 
*Tip Maestro:* Dale ambas fotos a Claude/ChatGPT y dile: *"Escribe el prompt de transición de video necesario para ir de la Imagen A a la Imagen B"*. 

¡Cópialo, pégalo, y obtén tu video!
