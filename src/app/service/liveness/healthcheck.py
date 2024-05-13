import httpx

from settings.config import (
    LIVENESS_URL,
)

expected_response = {
    'closed_eye': False,
    'face_in_center': True,
    'face_looking_forward': True,
    'face_rotation': {
        'roll': 0,
        'pitch': -4,
        'yaw': -6
    },
    'face_direction': 'forward',
}

with open('/media/liveness/face_photo.jpg', 'rb') as f:
    face_photo = f.read()
files = {'face_photo': face_photo}


async def send_liveness_request() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{LIVENESS_URL}/face-details/',
            files=files,
        )
        return response


async def liveness_healthcheck() -> (bool, int):
    response = await send_liveness_request()
    status_code = response.status_code
    if status_code == 200:
        return (
            response.json() == expected_response,
            status_code
        )
    return False, status_code
