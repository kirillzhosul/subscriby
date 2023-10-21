import requests

from app.settings import Settings


def api_call(method: str, params: dict) -> dict | None:
    """
    Calls API and returns JSON response or None if error.
    """
    try:
        method_url = f"{Settings().subscriby_api_url}/{method}"
        request = requests.get(url=method_url, params=params).json()
        if "error" in request:
            print(f"[ERROR]: API respond with error: {request['error']}")
            raise ValueError
        return request
    except Exception as e:
        print(f"[ERROR]: API unable to respond due to: {e}")
        return None
