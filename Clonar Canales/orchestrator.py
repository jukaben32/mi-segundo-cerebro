import os
import re
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

load_dotenv()

class ProductionBrain:
    def __init__(self):
        self.api_key_eleven = os.getenv("ELEVENLABS_API_KEY")
        self.api_key_fal = os.getenv("FAL_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgnuMvscL7PR")
        self.output_dir = Path("output")
        self.assets_dir = Path("assets")
        self.designs_dir = Path("designs")
        
        # Crear directorios si no existen
        self.output_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
        self.designs_dir.mkdir(exist_ok=True)

    def get_style_tokens(self, style_name="coldfusion"):
        """Carga los tokens de un sistema de diseño específico."""
        style_file = self.designs_dir / f"{style_name}.design.md"
        if not style_file.exists():
            print(f"⚠️ Estilo {style_name} no encontrado en /designs. Usando valores por defecto.")
            return ""
        
        content = style_file.read_text(encoding="utf-8")
        # Extraer directivas de prompts
        directives = re.findall(r'- "(.*?)"', content)
        return " ".join(directives)

    def parse_script(self, file_path):
        """Extrae el guion puro de un archivo Markdown, eliminando marcadores SFX/BGM para la locución."""
        print(f"📖 Leyendo guion de: {file_path}")
        content = Path(file_path).read_text(encoding="utf-8")
        
        # Buscar la sección del guion (Estado 8 o similar)
        if "## 4. GUION COMPLETO" in content:
            script_section = content.split("## 4. GUION COMPLETO")[1]
        else:
            script_section = content

        # Limpiar marcadores técnicos para el narrador
        clean_script = re.sub(r'\[SFX:.*?\]', '', script_section)
        clean_script = re.sub(r'\[BGM:.*?\]', '', clean_script)
        clean_script = re.sub(r'\[Pausa.*?\]', '...', clean_script)
        clean_script = re.sub(r'\*\*(.*?)\*\*:', '', clean_script) # Elimina (VOICEOVER):
        clean_script = re.sub(r'\[Tono.*?\]', '', clean_script)
        
        return clean_script.strip()

    def generate_audio(self, text, filename="narracion_completa.mp3"):
        """Envía el texto a ElevenLabs para generar la voz."""
        if not self.api_key_eleven or "tu_api_key" in self.api_key_eleven:
            print("❌ Error: Falta ELEVENLABS_API_KEY en el archivo .env")
            return

        print(f"🎙️ Generando voz con ElevenLabs (Voz ID: {self.voice_id})...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key_eleven
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            output_path = self.assets_dir / filename
            output_path.write_bytes(response.content)
            print(f"✅ Audio guardado en: {output_path}")
            return output_path
        else:
            print(f"❌ Error en ElevenLabs: {response.status_code} - {response.text}")

    def parse_video_prompts(self, file_path):
        """Extrae los prompts de video del archivo .md"""
        print(f"🔍 Buscando prompts en: {file_path}")
        content = Path(file_path).read_text(encoding="utf-8")
        
        # Busca patrones tipo: Prompt: [Contenido] o `[Contenido]`
        prompts = re.findall(r'(?:Prompt: |`)(.*?)(?:`|\n|$)', content)
        
        # Filtrar líneas vacías o demasiado cortas
        prompts = [p.strip() for p in prompts if len(p.strip()) > 10]
        
        return prompts

    def generate_video_clip(self, prompt, index):
        """Envía un prompt a Fal.ai usando Seedance 2.0 (u otro modelo configurado)."""
        if not self.api_key_fal or "tu_api_key" in self.api_key_fal:
            print("❌ Error: Falta FAL_KEY en el archivo .env")
            return

        print(f"🎬 Generando Clip {index}...")
        
        # Usando Seedance 2.0 via Fal.ai
        url = "https://fal.run/bytedance/seedance-2.0/text-to-video"
        headers = {
            "Authorization": f"Key {self.api_key_fal}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "resolution": "720p",
            "duration": "4",
            "aspect_ratio": "16:9"
        }

        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("video", {}).get("url")
            if video_url:
                print(f"📥 Descargando Clip {index}...")
                video_data = requests.get(video_url).content
                video_path = self.assets_dir / f"clip_{index:03d}.mp4"
                video_path.write_bytes(video_data)
                print(f"✅ Clip {index} guardado.")
                return video_path
        else:
            print(f"❌ Error en Fal.ai: {response.status_code} - {response.text}")

# --- INTERFAZ DE LÍNEA DE COMANDOS ---
if __name__ == "__main__":
    import sys
    brain = ProductionBrain()
    
    print("\n🧠 --- CEREBRO DE PRODUCCIÓN v1.0 ---")
    print("1. Generar VOICEOVER completo")
    print("2. Generar CLIPS DE VIDEO (Prueba: primeros 3)")
    print("3. Generar TODOS los clips (¡Cuidado con el presupuesto!)")
    print("q. Salir")
    
    choice = input("\nSelecciona una opción: ")
    
    if choice == "1":
        script_file = "The_Trillion_Dollar_Lie_Capitulo_Final.md"
        text = brain.parse_script(script_file)
        brain.generate_audio(text)
    
    elif choice == choice in ["2", "3"]:
        prompt_file = "The_Trillion_Dollar_Lie_Video_Prompts.md"
        prompts = brain.parse_video_prompts(prompt_file)
        limit = 3 if choice == "2" else len(prompts)
        
        print(f"Encontrados {len(prompts)} prompts. Procesando los primeros {limit}...")
        for i, p in enumerate(prompts[:limit]):
            brain.generate_video_clip(p, i+1)
            
    elif choice == "q":
        sys.exit()
