# Test básico para el flujo principal
import os
import subprocess

def test_main():
    # Ejecuta el flujo con un prompt de prueba
    resultado = subprocess.run(["python", "main.py", "Crea un guion para un video de prueba"], capture_output=True, text=True)
    assert os.path.exists("video_final.mp4"), "No se generó el video final"
    print("Test exitoso: video_final.mp4 generado")

if __name__ == "__main__":
    test_main()
