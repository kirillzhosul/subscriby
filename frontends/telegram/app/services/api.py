import requests

from app.settings import Settings


def api_call(method: str, params: dict) -> dict | None:
    """
    Calls API and returns JSON response or None if error.
    """
    method_url = f"{Settings().subscriby_api_url}/{method}"
    print(f"Calling {method_url}!")
    try:
        request = requests.get(url=method_url, params=params)
    except requests.exceptions.RequestException as e:
        return print(f"[ERROR]: Unable to send API request due to {e}!")
    try:
        json = request.json()
    except Exception as e:
        return print(
            f"[ERROR]: Unable to parse API JSON due to {e}, response: {request.text}!"
        )

    if "error" in json:
        return print(f"[ERROR]: API respond with error: {json['error']}!")

    return json
