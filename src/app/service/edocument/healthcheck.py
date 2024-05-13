import httpx

from settings.config import (
    EDOCUMENT_URL,
    EDOCUMENT_API_KEY,
    PERSONAL_ID_NUMBER,
    PHONE_NUMBER,
)

expected_response = {
    'is_verified': True,
}

headers = {
    'X-API-KEY': EDOCUMENT_API_KEY,
    'Content-Type': 'application/json',
}

json = {
    'iin': PERSONAL_ID_NUMBER,
    'phone': PHONE_NUMBER,
}


async def send_edocument_request() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{EDOCUMENT_URL}/api/v1/e-document/mcdb/check',
            headers=headers,
            json=json,
            timeout=30,
        )
        return response


async def edocument_healthcheck() -> (bool, int):
    status_code = 400
    for i in range(3):
        response = await send_edocument_request()
        status_code = response.status_code
        if status_code == 200:
            return (
                response.json() == expected_response,
                status_code,
            )
    return False, status_code
