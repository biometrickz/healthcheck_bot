import httpx

from settings.config import (
    EDOCUMENT_URL,
    EDOCUMENT_API_KEY,
    PERSONAL_ID_NUMBER,
)

expected_response = {
    'narcological_account': {
        'RU': 'Не состоит на учете в наркологической организации',
        'KZ': 'Наркологиялық ұйымда диспансерлік есепте тұрмайды',
    },
    'psychoneurological_account': {
        'RU': 'Не состоит на учете в психоневрологической организации',
        'KZ': 'Психоневрологиялық ұйымда диспансерлік есепте тұрмайды',
    },
    'antitubercular_account': {
        'RU': 'Не состоит на учете в противотуберкулезной организации',
        'KZ': 'Туберкулезге қарсы ұйымда диспансерлік есепте тұрмайды',
    },
}

headers = {
    'X-API-KEY': EDOCUMENT_API_KEY,
    'Content-Type': 'application/json',
}

json = {
    'iin': PERSONAL_ID_NUMBER,
}


async def send_dispensary_request() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{EDOCUMENT_URL}/api/v1/e-document/dispenser/check',
            headers=headers,
            json=json,
            timeout=30,
        )
        return response


async def dispensary_healthcheck() -> (bool, int):
    status_code = 400
    for i in range(3):
        response = await send_dispensary_request()
        status_code = response.status_code
        if status_code == 200:
            return (
                response.json() == expected_response,
                status_code,
            )
    return False, status_code
