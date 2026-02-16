from adapters.sl_client import APIClient


_api_client_instance = None

def get_api_client() -> APIClient:
    global _api_client_instance

    if _api_client_instance is None:
        _api_client_instance = APIClient()

    return _api_client_instance
