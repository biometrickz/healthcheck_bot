import httpx

from decimal import Decimal
from settings.config import (
    FACE2FACE_URL,
)

expected_response = {
    'result': True,
    'prediction': Decimal(0.9941255796088875),
    'cosine_distance': Decimal(0.2535792589187622),
}

with open('/media/face2face/image_1.jpg', 'rb') as f:
    image_1 = f.read()
with open('/media/face2face/image_2.jpg', 'rb') as f:
    image_2 = f.read()
files = {
    'image_1': image_1,
    'image_2': image_2,
}


async def send_face2face_request() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{FACE2FACE_URL}/verify',
            files=files,
            timeout=30,
        )
        return response


async def face2face_healthcheck() -> (bool, int):
    response = await send_face2face_request()
    status_code = response.status_code
    if status_code == 200:
        return (
            response.json() == expected_response,
            status_code,
        )
    return False, status_code
