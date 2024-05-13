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


class HealthChecker:
    __timeout = 10

    def __init__(self):
        self.is_liveness_healthy: bool = True
        self.liveness_code: int = 200
        self.is_face2face_healthy: bool = True
        self.face2face_code: int = 200
        self.is_doc_recognition_healthy: bool = True
        self.doc_recognition_code: int = 200
        self.is_edocument_healthy: bool = True
        self.edocument_code: int = 200
        self.is_addresses_healthy: bool = True
        self.addresses_code: int = 200
        self.is_dispensary_healthy: bool = True
        self.dispensary_code: int = 200
        self.is_qamqor_healthy: bool = True
        self.qamqor_code: int = 200

    async def check_is_liveness_healthy(self):
        try:
            status, code = await liveness_healthcheck()
            if status and code == 200:
                self.is_liveness_healthy = True
            else:
                self.is_liveness_healthy = False
            self.liveness_code = code
        except httpx.RequestError:
            self.is_liveness_healthy = False
            self.liveness_code = 500

    async def check_is_face2face_healthy(self):
        try:
            status, code = await face2face_healthcheck()
            if status and code == 200:
                self.is_face2face_healthy = True
            else:
                self.is_face2face_healthy = False
            self.face2face_code = code
        except httpx.RequestError:
            self.is_face2face_healthy = False
            self.face2face_code = 500

    async def check_is_doc_rec_healthy(self):
        try:
            response = httpx.get(
                url=f'{DOC_RECOGNITION_URL}/healthcheck',
                timeout=self.__timeout,
            )
            status_code = response.status_code
            if status_code == 200:
                self.is_doc_recognition_healthy = True
            else:
                self.is_doc_recognition_healthy = False
            self.doc_recognition_code = status_code
        except httpx.RequestError:
            self.is_doc_recognition_healthy = False
            self.doc_recognition_code = 500

    async def check_is_edocument_healthy(self):
        try:
            status, code = await edocument_healthcheck()
            if status and code == 200:
                self.is_edocument_healthy = True
            else:
                self.is_edocument_healthy = False
            self.edocument_code = code
        except httpx.RequestError:
            self.is_edocument_healthy = False
            self.edocument_code = 500

    async def check_is_addresses_healthy(self):
        try:
            response = httpx.get(
                url=f'{ADDRESS_BASE_URL}/api/v1/government/healthcheck',
                timeout=self.__timeout,
            )
            status_code = response.status_code
            if status_code == 200:
                self.is_addresses_healthy = True
            else:
                self.is_addresses_healthy = False
            self.addresses_code = status_code
        except httpx.RequestError:
            self.is_addresses_healthy = False
            self.addresses_code = 500

    async def check_is_dispensary_healthy(self):
        try:
            status, code = await dispensary_healthcheck()
            if status and code == 200:
                self.is_dispensary_healthy = True
            else:
                self.is_dispensary_healthy = False
            self.dispensary_code = code
        except httpx.RequestError:
            self.is_dispensary_healthy = False
            self.dispensary_code = 500

    async def check_is_qamqor_healthy(self):
        try:
            response = httpx.get(
                url=f'{QAMQOR_FACE_SEARCH_BASE_URL}/healthcheck',
                timeout=self.__timeout,
            )
            status_code = response.status_code
            if status_code == 200:
                self.is_qamqor_healthy = True
            else:
                self.is_qamqor_healthy = False
            self.qamqor_code = status_code
        except httpx.RequestError:
            self.is_qamqor_healthy = False
            self.qamqor_code = 500

    async def check_all(self):
        await self.check_is_liveness_healthy()
        await self.check_is_face2face_healthy()
        await self.check_is_doc_rec_healthy()
        await self.check_is_edocument_healthy()
        # await self.check_is_addresses_healthy()
        await self.check_is_dispensary_healthy()
        # await self.check_is_qamqor_healthy()

    def get_statuses(self) -> dict:
        return {
            'is_liveness_healthy': self.is_liveness_healthy,
            'is_face2face_healthy': self.is_face2face_healthy,
            'is_doc_recognition_healthy': self.is_doc_recognition_healthy,
            'is_edocument_healthy': self.is_edocument_healthy,
            'is_addresses_healthy': self.is_addresses_healthy,
            'is_dispensary_healthy': self.is_dispensary_healthy,
            'is_qamqor_healthy': self.is_qamqor_healthy,
        }

    def get_codes(self) -> dict:
        return {
            'liveness_code': self.liveness_code,
            'face2face_code': self.face2face_code,
            'doc_recognition_code': self.doc_recognition_code,
            'edocument_code': self.edocument_code,
            'addresses_code': self.addresses_code,
            'dispensary_code': self.dispensary_code,
            'qamqor_code': self.qamqor_code,
        }

    def get_status_values(self):
        return [
            self.is_liveness_healthy,
            self.is_face2face_healthy,
            self.is_doc_recognition_healthy,
            self.is_edocument_healthy,
            self.is_addresses_healthy,
            self.is_dispensary_healthy,
            self.is_qamqor_healthy,
        ]


healthchecker = HealthChecker()
