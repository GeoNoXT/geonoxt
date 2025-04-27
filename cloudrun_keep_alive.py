import argparse
import requests
import sys

def main():
    parser = argparse.ArgumentParser(description="Hace una petición HTTP a una URL (para mantener despierto Cloud Run, por ejemplo).")
    parser.add_argument("url", help="URL del servicio a llamar")

    args = parser.parse_args()

    try:
        response = requests.get(args.url)
        print(f"Respuesta: {response.status_code}")
        sys.exit(0 if response.ok else 1)
    except Exception as e:
        print(f"Error al hacer la petición: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
