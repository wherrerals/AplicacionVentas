"""
Servicio de autenticación con Google (OpenID Connect).

Encapsula el flujo OAuth2/OIDC contra Google:
    1. Construir la URL de autorización (con parámetro ``state`` anti-CSRF).
    2. Intercambiar el ``code`` recibido por tokens.
    3. Verificar criptográficamente el ``id_token`` y validar que el usuario
       pertenezca al dominio corporativo (@ledstudio.cl).

No crea ni modifica usuarios: solo devuelve la identidad verificada de Google.
El vínculo con un ``User`` existente lo resuelve la capa de vistas.
"""

import logging
from urllib.parse import urlencode

import requests
from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

logger = logging.getLogger(__name__)

# Endpoints OIDC de Google
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"

# Scopes mínimos: identidad + correo
GOOGLE_SCOPES = ["openid", "email", "profile"]

# Tolerancia de reloj (segundos) al validar el id_token
CLOCK_SKEW_SECONDS = 10


class GoogleOAuthError(Exception):
    """Error recuperable del flujo OAuth (identidad inválida o rechazada)."""


def build_authorization_url(redirect_uri, state):
    """
    Construye la URL a la que se redirige al usuario para iniciar sesión.

    Args:
        redirect_uri (str): URL de callback registrada en Google Cloud.
        state (str): Token aleatorio guardado en sesión para validar el retorno.

    Returns:
        str: URL de autorización de Google.
    """
    params = {
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }

    # Restringe el selector de cuentas al dominio corporativo (mejor UX).
    dominio = getattr(settings, "GOOGLE_ALLOWED_DOMAIN", None)
    if dominio:
        params["hd"] = dominio

    return f"{GOOGLE_AUTH_URI}?{urlencode(params)}"


def exchange_code_for_tokens(code, redirect_uri):
    """
    Intercambia el ``code`` de autorización por tokens de Google.

    Args:
        code (str): Código de autorización devuelto por Google.
        redirect_uri (str): La misma redirect_uri usada al iniciar el flujo.

    Returns:
        dict: Respuesta del endpoint de token (incluye ``id_token``).

    Raises:
        GoogleOAuthError: Si Google rechaza el intercambio.
    """
    data = {
        "code": code,
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(GOOGLE_TOKEN_URI, data=data, timeout=10)
    except requests.RequestException as exc:
        raise GoogleOAuthError("No se pudo contactar a Google.") from exc

    if response.status_code != 200:
        # Google devuelve el motivo en el cuerpo (error / error_description).
        detalle = ""
        try:
            err = response.json()
            detalle = err.get("error") or ""
            if err.get("error_description"):
                detalle = f"{detalle}: {err['error_description']}"
        except ValueError:
            detalle = response.text[:200]
        logger.error(
            "Fallo en token exchange con Google (HTTP %s): %s",
            response.status_code,
            detalle,
        )
        raise GoogleOAuthError(
            f"Google rechazó el intercambio de credenciales ({detalle})."
        )

    payload = response.json()
    if "id_token" not in payload:
        raise GoogleOAuthError("La respuesta de Google no contiene id_token.")

    return payload


def verify_identity(id_token_str):
    """
    Verifica el ``id_token`` y valida el dominio corporativo.

    Comprueba firma, audiencia (client_id), emisor y expiración vía google-auth,
    y luego que el correo esté verificado y pertenezca al dominio permitido.

    Args:
        id_token_str (str): El id_token (JWT) recibido de Google.

    Returns:
        dict: Claims verificados. Interesan ``email``, ``hd`` y ``name``.

    Raises:
        GoogleOAuthError: Si el token es inválido o el dominio no está permitido.
    """
    try:
        claims = google_id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
            clock_skew_in_seconds=CLOCK_SKEW_SECONDS,
        )
    except ValueError as exc:
        raise GoogleOAuthError("El id_token de Google no es válido.") from exc

    if not claims.get("email_verified"):
        raise GoogleOAuthError("El correo de Google no está verificado.")

    email = (claims.get("email") or "").lower()
    dominio = getattr(settings, "GOOGLE_ALLOWED_DOMAIN", "").lower()

    # Doble chequeo de dominio: claim `hd` y sufijo del correo.
    if dominio:
        hd = (claims.get("hd") or "").lower()
        if hd != dominio or not email.endswith(f"@{dominio}"):
            raise GoogleOAuthError(
                f"Solo se permite el acceso con cuentas @{dominio}."
            )

    return claims
