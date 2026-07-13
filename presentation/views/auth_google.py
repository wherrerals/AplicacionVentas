"""
Vistas del login con Google (OpenID Connect).

Flujo:
    google_login    -> genera `state`, arma la URL de Google y redirige.
    google_callback -> valida `state`, verifica la identidad y VINCULA el correo
                       a un ``User`` YA EXISTENTE. Nunca crea usuarios nuevos.
"""

import logging
import secrets

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from domain.services.google_oauth import (
    GoogleOAuthError,
    build_authorization_url,
    exchange_code_for_tokens,
    verify_identity,
)

logger = logging.getLogger(__name__)

SESSION_STATE_KEY = "google_oauth_state"
SESSION_NEXT_KEY = "google_oauth_next"
LOGIN_TEMPLATE = "registration/login.html"
# Backend explícito: login() lo necesita porque no autenticamos vía ModelBackend.
AUTH_BACKEND = "django.contrib.auth.backends.ModelBackend"


def _callback_redirect_uri(request):
    """URL de callback absoluta; debe coincidir con la registrada en Google."""
    return request.build_absolute_uri(reverse("google_callback"))


def _find_existing_user(email):
    """
    Busca un usuario existente por correo (o username, que en esta app coincide).
    No crea usuarios. Devuelve None si no hay coincidencia.
    """
    user = User.objects.filter(email__iexact=email).first()
    if user is None:
        user = User.objects.filter(username__iexact=email).first()
    return user


def google_login(request):
    """Inicia el flujo OAuth: guarda `state` en sesión y redirige a Google."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        logger.error("GOOGLE_OAUTH_CLIENT_ID no está configurado.")
        return render(
            request,
            LOGIN_TEMPLATE,
            {"google_error": "El acceso con Google no está configurado."},
            status=500,
        )

    state = secrets.token_urlsafe(32)
    request.session[SESSION_STATE_KEY] = state

    # Preserva ?next= si es una URL interna segura.
    next_url = request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        request.session[SESSION_NEXT_KEY] = next_url

    auth_url = build_authorization_url(_callback_redirect_uri(request), state)
    return redirect(auth_url)


def google_callback(request):
    """Valida el retorno de Google y vincula con un usuario existente."""
    # Google puede devolver un error (p. ej. el usuario canceló).
    if request.GET.get("error"):
        return render(
            request,
            LOGIN_TEMPLATE,
            {"google_error": "No se completó el inicio de sesión con Google."},
        )

    # Validación anti-CSRF del state.
    expected_state = request.session.pop(SESSION_STATE_KEY, None)
    received_state = request.GET.get("state")
    if not expected_state or expected_state != received_state:
        logger.warning("State inválido en callback de Google OAuth.")
        return render(
            request,
            LOGIN_TEMPLATE,
            {"google_error": "La sesión de inicio expiró. Inténtalo de nuevo."},
        )

    code = request.GET.get("code")
    if not code:
        return render(
            request,
            LOGIN_TEMPLATE,
            {"google_error": "No se recibió el código de autorización."},
        )

    try:
        tokens = exchange_code_for_tokens(code, _callback_redirect_uri(request))
        claims = verify_identity(tokens["id_token"])
    except GoogleOAuthError as exc:
        return render(request, LOGIN_TEMPLATE, {"google_error": str(exc)})

    email = (claims.get("email") or "").lower()
    user = _find_existing_user(email)

    if user is None:
        logger.info("Login Google rechazado: %s sin usuario asociado.", email)
        return render(
            request,
            LOGIN_TEMPLATE,
            {
                "google_error": (
                    "Tu cuenta no está registrada en Studio GO. "
                    "Contacta al administrador."
                )
            },
        )

    if not user.is_active:
        return render(
            request,
            LOGIN_TEMPLATE,
            {"google_error": "Tu cuenta está deshabilitada."},
        )

    login(request, user, backend=AUTH_BACKEND)
    logger.info("Login Google exitoso: %s (user_id=%s).", email, user.pk)

    next_url = request.session.pop(SESSION_NEXT_KEY, None)
    return redirect(next_url or settings.LOGIN_REDIRECT_URL)
