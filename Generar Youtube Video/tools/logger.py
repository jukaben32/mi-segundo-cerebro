# logger.py
# Utilidad simple para logging en los scripts

import datetime

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] {msg}\n")
    print(f"[{now}] {msg}")
