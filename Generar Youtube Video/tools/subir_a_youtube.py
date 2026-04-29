# Script: subir_a_youtube.py
# Sube el video generado automáticamente a YouTube usando la API de YouTube Data v3
# Uso: python tools/subir_a_youtube.py video_final.mp4 "Título" "Descripción"

import sys

# NOTA: Este script es un ejemplo. Para funcionar, debes crear credenciales en Google Cloud Console y descargar client_secrets.json
# Instala la librería: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Autenticación
creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

youtube = build("youtube", "v3", credentials=creds)

video_file = sys.argv[1] if len(sys.argv) > 1 else "video_final.mp4"
title = sys.argv[2] if len(sys.argv) > 2 else "Short generado automáticamente"
description = sys.argv[3] if len(sys.argv) > 3 else "Video creado con el generador automático de shorts."

request_body = {
    "snippet": {
        "categoryId": "22",
        "title": title,
        "description": description
    },
    "status": {
        "privacyStatus": "private"
    }
}

mediaFile = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/*")

print("Subiendo video a YouTube...")
response_upload = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=mediaFile
).execute()

print("Video subido! ID:", response_upload["id"])
