import httpx

from app.service.liveness.healthcheck import liveness_healthcheck
from app.service.face2face.healthcheck import face2face_healthcheck
from app.service.edocument.healthcheck import edocument_healthcheck

from settings.config import (
    LIVENESS_URL,
    FACE2FACE_URL,
    DOC_RECOGNITION_URL,
    EDOCUMENT_URL,
    DISPENSARY_BASE_URL,
    ADDRESS_BASE_URL,
    QAMQOR_FACE_SEARCH_BASE_URL,
)


class HealthChecker:
    __timeout = 10

    def __init__(self):
        self.is_liveness_healthy = True
        self.is_face2face_healthy = True
        self.is_doc_recognition_healthy = True
        self.is_edocument_healthy = True
        self.is_addresses_healthy = True
        self.is_dispensary_healthy = True
        self.is_qamqor_healthy = True

    async def check_is_liveness_healthy(self):
        try:
            response = httpx.get(
                url=f'{LIVENESS_URL}/healthcheck',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_liveness_healthy = True
            else:
                result = await liveness_healthcheck()
                if not result[0]:
                    self.is_liveness_healthy = False

        except httpx.RequestError:
            self.is_liveness_healthy = False

    async def check_is_face2face_healthy(self):
        try:
            response = httpx.get(
                url=f'{FACE2FACE_URL}/healthcheck',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_face2face_healthy = True
            else:
                result = await face2face_healthcheck()
                if not result[0]:
                    self.is_face2face_healthy = False
        except httpx.RequestError:
            self.is_face2face_healthy = False

    def check_is_doc_rec_healthy(self):
        try:
            response = httpx.get(
                url=f'{DOC_RECOGNITION_URL}/healthcheck',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_doc_recognition_healthy = True
            else:
                self.is_doc_recognition_healthy = False
        except httpx.RequestError:
            self.is_doc_recognition_healthy = False

    async def check_is_edocument_healthy(self):
        try:
            response = httpx.get(
                url=f'{EDOCUMENT_URL}/api/v1/e-document/healthcheck/',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_edocument_healthy = True
            else:
                result = await edocument_healthcheck()
                if not result[0]:
                    self.is_edocument_healthy = False
        except httpx.RequestError:
            self.is_edocument_healthy = False

    def check_is_addresses_healthy(self):
        try:
            response = httpx.get(
                url=f'{ADDRESS_BASE_URL}/api/v1/government/healthcheck',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_addresses_healthy = True
            else:
                self.is_addresses_healthy = False
        except httpx.RequestError:
            self.is_addresses_healthy = False

    def check_is_dispensary_healthy(self):
        try:
            response = httpx.get(
                url=f'{DISPENSARY_BASE_URL}/api/v1/e-document/healthcheck/',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_dispensary_healthy = True
            else:
                self.is_dispensary_healthy = False
        except httpx.RequestError:
            self.is_dispensary_healthy = False

    def check_is_qamqor_healthy(self):
        try:
            response = httpx.get(
                url=f'{QAMQOR_FACE_SEARCH_BASE_URL}/healthcheck',
                timeout=self.__timeout,
            )
            if response.status_code == 200:
                self.is_qamqor_healthy = True
            else:
                self.is_qamqor_healthy = False
        except httpx.RequestError:
            self.is_qamqor_healthy = False

    async def check_all(self):
        await self.check_is_liveness_healthy()
        await self.check_is_face2face_healthy()
        self.check_is_doc_rec_healthy()
        await self.check_is_edocument_healthy()
        # self.check_is_addresses_healthy()
        self.check_is_dispensary_healthy()
        # self.check_is_qamqor_healthy()

    def get_status(self):
        return self.__dict__

    def get_status_values(self):
        return self.__dict__.values()


healthchecker = HealthChecker()
