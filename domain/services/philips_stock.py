"""
Servicio de lectura del Google Sheet ``philips_stock_transito``.

Lee (solo lectura) la hoja de cálculo con una cuenta de servicio de Google y
devuelve las filas ya normalizadas para el reporte. No persiste nada: es un
previsualizador informativo. Reutiliza ``google-auth`` (ya instalado) y llama
directamente a la API REST de Sheets, sin dependencias nuevas.

Estructura esperada de la hoja (dos filas de encabezado):
    Fila 1: encabezados agrupadores (``Stock disponible``, ``En espera de QR``…).
    Fila 2: encabezados reales (``12NC``, ``12NC DESCR.``, ``BG``,
            ``Storage 01``, ``Certificaciones``, ``jul``, ``ago``, ``sept``…).
    Fila 3+: datos.

Las columnas de meses (desde ``Storage 01`` en adelante son fijas; los meses
son dinámicos) se leen según su cantidad en la fila de encabezado, de modo que
si aparecen meses nuevos salen solos sin tocar código.
"""

import logging
from urllib.parse import quote

from django.conf import settings
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

# Solo lectura.
SHEETS_SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHEETS_VALUES_URL = (
    "https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{rango}"
)

# Índices de columnas fijas (0-indexed) según la estructura de la hoja.
COL_CODIGO = 0          # 12NC
COL_DESCRIPCION = 1     # 12NC DESCR.
COL_BG = 2              # BG
COL_STOCK = 3           # Storage 01 (Stock disponible)
COL_CERTIFICACION = 4   # Certificaciones (En espera de QR)
PRIMERA_COL_MES = 5     # jul, ago, sept, ... (dinámico)

# La hoja trae 2 filas de encabezado; la fila 2 (índice 1) tiene los nombres.
FILA_ENCABEZADO = 1
PRIMERA_FILA_DATOS = 2


class PhilipsStockError(Exception):
    """Error recuperable al leer el Sheet de Philips."""


def _cargar_credenciales():
    """
    Construye las credenciales de la cuenta de servicio.

    Admite que ``GOOGLE_SA_CREDENTIALS`` sea la ruta a un archivo ``.json`` o
    el contenido JSON inline (útil para montar el secreto por variable de
    entorno en Docker).
    """
    raw = getattr(settings, "GOOGLE_SA_CREDENTIALS", None)
    if not raw:
        raise PhilipsStockError("GOOGLE_SA_CREDENTIALS no está configurado.")

    raw = raw.strip()
    try:
        if raw.startswith("{"):
            import json

            info = json.loads(raw)
            return service_account.Credentials.from_service_account_info(
                info, scopes=SHEETS_SCOPE
            )
        return service_account.Credentials.from_service_account_file(
            raw, scopes=SHEETS_SCOPE
        )
    except (ValueError, OSError) as exc:
        logger.exception("No se pudieron cargar las credenciales de la cuenta de servicio.")
        raise PhilipsStockError(
            "Las credenciales de Google (GOOGLE_SA_CREDENTIALS) no son válidas."
        ) from exc


def _celda(fila, idx):
    """Valor de la celda en ``idx`` o cadena vacía si la fila es más corta."""
    if idx < len(fila):
        valor = fila[idx]
        return "" if valor is None else valor
    return ""


def _es_negativo(valor):
    """True si el valor representa un número negativo."""
    if isinstance(valor, bool):
        return False
    if isinstance(valor, (int, float)):
        return valor < 0
    try:
        return float(str(valor).strip()) < 0
    except (ValueError, TypeError):
        return False


def obtener_stock_transito():
    """
    Lee el Sheet y devuelve los datos normalizados para el template.

    Returns:
        dict: {
            "meses": ["jul", "ago", "sept", ...],
            "filas": [
                {
                    "codigo": str, "descripcion": str, "bg": str,
                    "stock": valor, "stock_negativo": bool,
                    "certificacion": valor, "meses": [valor, ...],
                },
                ...
            ],
        }

    Raises:
        PhilipsStockError: si falta configuración o la API falla.
    """
    sheet_id = getattr(settings, "PHILIPS_SHEET_ID", None)
    rango = getattr(settings, "PHILIPS_SHEET_RANGE", "Hoja 1")
    if not sheet_id:
        raise PhilipsStockError("PHILIPS_SHEET_ID no está configurado.")

    url = SHEETS_VALUES_URL.format(sheet_id=sheet_id, rango=quote(rango))

    try:
        creds = _cargar_credenciales()
        session = AuthorizedSession(creds)
        # UNFORMATTED_VALUE: devuelve los números tal cual (permite negativos y cálculo).
        resp = session.get(
            url, params={"valueRenderOption": "UNFORMATTED_VALUE"}, timeout=15
        )
    except PhilipsStockError:
        raise
    except Exception as exc:  # noqa: BLE001 - se degrada a un error controlado
        logger.exception("Fallo de red al leer el Sheet de Philips.")
        raise PhilipsStockError("No se pudo contactar a Google Sheets.") from exc

    if resp.status_code != 200:
        logger.error(
            "Sheets API respondió HTTP %s: %s", resp.status_code, resp.text[:300]
        )
        if resp.status_code == 403:
            raise PhilipsStockError(
                "Google denegó el acceso. ¿Compartiste el Sheet con el correo de "
                "la cuenta de servicio (Lector) y habilitaste la Google Sheets API?"
            )
        if resp.status_code == 404:
            raise PhilipsStockError(
                "No se encontró el Sheet o la hoja indicada. Revisa PHILIPS_SHEET_ID "
                "y PHILIPS_SHEET_RANGE."
            )
        raise PhilipsStockError(
            f"Google Sheets respondió {resp.status_code} al leer los datos."
        )

    values = resp.json().get("values", [])
    if len(values) <= PRIMERA_FILA_DATOS:
        return {"meses": [], "filas": []}

    encabezado = values[FILA_ENCABEZADO]
    meses = [str(h).strip() for h in encabezado[PRIMERA_COL_MES:] if str(h).strip()]

    filas = []
    for fila in values[PRIMERA_FILA_DATOS:]:
        # Ignora filas totalmente vacías.
        if not any(str(c).strip() for c in fila):
            continue
        codigo = str(_celda(fila, COL_CODIGO)).strip()
        if not codigo:
            continue

        stock = _celda(fila, COL_STOCK)
        filas.append(
            {
                "codigo": codigo,
                "descripcion": str(_celda(fila, COL_DESCRIPCION)).strip(),
                "bg": str(_celda(fila, COL_BG)).strip(),
                "stock": stock,
                "stock_negativo": _es_negativo(stock),
                "certificacion": _celda(fila, COL_CERTIFICACION),
                "meses": [_celda(fila, PRIMERA_COL_MES + i) for i in range(len(meses))],
            }
        )

    return {"meses": meses, "filas": filas}
