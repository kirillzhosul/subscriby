from aiohttp import ClientSession

from app.settings import SubscribySettings


async def api_call(method: str, params: dict) -> dict | None:
    """
    Calls API and returns JSON response or None if error.
    """
    settings = SubscribySettings()
    if settings.auth_method == "secret":
        params |= {"secret": settings.auth_secret}
    try:
        async with ClientSession() as session:
            async with session.get(
                f"{SubscribySettings().api_host}/{method}",
                params=params,
            ) as response:
                if response.status != 200:
                    return print(
                        f"[ERROR]: API respond with status: {response.status}!"
                    )
                json = await response.json()
                if "error" in json:
                    return print(f"[ERROR]: API respond with error: {json['error']}!")
                return json
    except Exception as e:
        return print(f"[ERROR]: Unable to send API request due to {e}!")
