import asyncio

import httpx

from app.service.dispensary.healthcheck import dispensary_healthcheck
from app.service.edocument.healthcheck import edocument_healthcheck
from app.service.face2face.healthcheck import face2face_healthcheck
from app.service.liveness.healthcheck import liveness_healthcheck

from settings.config import (
    ADDRESS_BASE_URL,
    DOC_RECOGNITION_URL,
    QAMQOR_FACE_SEARCH_BASE_URL,
)


class ServiceStatus:
    def __init__(
            self,
            is_healthy: bool = True,
            status_code: int = 200
    ):
        self.is_healthy: bool = is_healthy
        self.status_code: int = status_code


class HealthChecker:
    __timeout__ = 30

    def __init__(self):
        self.liveness: ServiceStatus = ServiceStatus()
        self.face2face: ServiceStatus = ServiceStatus()
        self.doc_recognition: ServiceStatus = ServiceStatus()
        self.edocument: ServiceStatus = ServiceStatus()
        self.ekyzmet: ServiceStatus = ServiceStatus()
        self.dispensary: ServiceStatus = ServiceStatus()
        self.qamqor: ServiceStatus = ServiceStatus()

    async def check_is_liveness_healthy(self):
        try:
            status, code = await liveness_healthcheck()
            if status and code == 200:
                self.liveness.is_liveness_healthy = True
            else:
                self.liveness.is_liveness_healthy = False
            self.liveness.status_code = code
        except httpx.RequestError:
            self.liveness.is_healthy = False
            self.liveness.status_code = 500

    async def check_is_face2face_healthy(self):
        try:
            status, code = await face2face_healthcheck()
            if status and code == 200:
                self.face2face.is_healthy = True
            else:
                self.face2face.is_healthy = False
            self.face2face.status_code = code
        except httpx.RequestError:
            self.face2face.is_healthy = False
            self.face2face.status_code = 500

    async def check_is_doc_rec_healthy(self):
        try:
            async with httpx.AsyncClient(
                    timeout=self.__timeout__
            ) as client:
                response = await client.get(
                    f'{DOC_RECOGNITION_URL}/healthcheck'
                )
            status_code = response.status_code
            if status_code == 200:
                self.doc_recognition.is_healthy = True
            else:
                self.doc_recognition.is_healthy = False
            self.doc_recognition.status_code = status_code
        except httpx.RequestError:
            self.doc_recognition.is_healthy = False
            self.doc_recognition.status_code = 500

    async def check_is_edocument_healthy(self):
        try:
            status, code = await edocument_healthcheck()
            if status and code == 200:
                self.edocument.is_healthy = True
            else:
                self.edocument.is_healthy = False
            self.edocument.status_code = code
        except httpx.RequestError:
            self.edocument.is_healthy = False
            self.edocument.status_code = 500

    async def check_is_addresses_healthy(self):
        try:
            async with httpx.AsyncClient(
                    timeout=self.__timeout__
            ) as client:
                response = await client.get(
                    url=f'{ADDRESS_BASE_URL}/api/v1/government/healthcheck'
                )
            status_code = response.status_code
            if status_code == 200:
                self.ekyzmet.is_healthy = True
            else:
                self.ekyzmet.is_healthy = False
            self.ekyzmet.status_code = status_code
        except httpx.RequestError:
            self.ekyzmet.is_healthy = False
            self.ekyzmet.status_code = 500

    async def check_is_dispensary_healthy(self):
        try:
            status, code = await dispensary_healthcheck()
            if status and code == 200:
                self.dispensary.is_healthy = True
            else:
                self.dispensary.is_healthy = False
            self.dispensary.status_code = code
        except httpx.RequestError:
            self.dispensary.is_healthy = False
            self.dispensary.status_code = 500

    async def check_is_qamqor_healthy(self):
        try:
            async with httpx.AsyncClient(
                    timeout=self.__timeout__
            ) as client:
                response = await client.get(
                    url=f'{QAMQOR_FACE_SEARCH_BASE_URL}/healthcheck'
                )
            status_code = response.status_code
            if status_code == 200:
                self.qamqor.is_healthy = True
            else:
                self.qamqor.is_healthy = False
            self.qamqor.status_code = status_code
        except httpx.RequestError:
            self.qamqor.is_healthy = False
            self.qamqor.status_code = 500

    async def check_all(self):
        await asyncio.gather(
            self.check_is_liveness_healthy(),
            self.check_is_face2face_healthy(),
            self.check_is_doc_rec_healthy(),
            self.check_is_edocument_healthy(),
            # self.check_is_addresses_healthy(),
            self.check_is_dispensary_healthy(),
            # self.check_is_qamqor_healthy()
        )

    def get_statuses(self) -> dict:
        return {
            'is_liveness_healthy': self.liveness.is_healthy,
            'is_face2face_healthy': self.face2face.is_healthy,
            'is_doc_recognition_healthy': self.doc_recognition.is_healthy,
            'is_edocument_healthy': self.edocument.is_healthy,
            'is_addresses_healthy': self.ekyzmet.is_healthy,
            'is_dispensary_healthy': self.dispensary.is_healthy,
            'is_qamqor_healthy': self.qamqor.is_healthy,
        }

    def get_codes(self) -> dict:
        return {
            'liveness_code': self.liveness.status_code,
            'face2face_code': self.face2face.status_code,
            'doc_recognition_code': self.doc_recognition.status_code,
            'edocument_code': self.edocument.status_code,
            'addresses_code': self.ekyzmet.status_code,
            'dispensary_code': self.dispensary.status_code,
            'qamqor_code': self.qamqor.status_code,
        }

    def get_status_values(self):
        return self.get_statuses().values()


healthchecker = HealthChecker()
