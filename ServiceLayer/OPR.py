import httpx

import httpx

try:
    # Realizar una solicitud HTTP que genere un error de timeout
    response_timeout = httpx.get('https://httpbin.org/status/503')
    response_timeout.raise_for_status()  # Generará una excepción HTTPStatusError para un timeout
    if response_timeout.status_code == 503:
        print("Service Unavailable")
except httpx.TimeoutException as exc:
    print(f"Error de tiempo de espera: {exc}")
    print(f"Código de estado HTTP: {exc}")
except httpx.HTTPStatusError as exc:
    print(f"Se produjo un error HTTP: {exc}")
    print(f"Código de estado HTTP: {exc.response.status_code}")
    print(f"Mensaje de error: {exc.response.text}")
except httpx.NetworkError as exc:
    print(f"Error de red: {exc}")
except Exception as exc:
    print(f"Error desconocido: {exc}")
