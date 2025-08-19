#!/usr/bin/env python3
import requests
import sys

URL = "http://127.0.0.1/metrics/"

def get_metric(metric_name):
    try:
        r = requests.get(URL, timeout=3)
        for line in r.text.splitlines():
            if line.startswith(metric_name):
                parts = line.split()
                if len(parts) == 2:
                    print(parts[1])
                    return
        print("0")  # métrica não encontrada
    except Exception:
        print("0")  # erro ao conectar

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: metric_django.py <nome_da_metrica>")
    else:
        get_metric(sys.argv[1])
