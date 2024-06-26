from decouple import config

# Telegram
TOKEN: str = config('TOKEN', cast=str)

# Redis
REDIS_HOST: str = config('REDIS_HOST', cast=str)
REDIS_CONTAINER_PORT: int = config('REDIS_CONTAINER_PORT', cast=int)
REDIS_HOST_PORT: int = config('REDIS_HOST_PORT', cast=int)
REDIS_DB: int = config('REDIS_DB', cast=int)

# Liveness
LIVENESS_URL: str = config('LIVENESS_URL', cast=str)

# Doc recognition
DOC_RECOGNITION_URL: str = config('DOC_RECOGNITION_URL', cast=str)

# F2F
FACE2FACE_URL = config('FACE2FACE_URL', cast=str)

# EDocument
EDOCUMENT_URL: str = config('EDOCUMENT_BASE_URL', cast=str)
EDOCUMENT_API_KEY: str = config('EDOCUMENT_API_KEY', cast=str)

# EDocument
EDOCUMENT_V2_URL: str = config('EDOCUMENT_V2_BASE_URL', cast=str)
EDOCUMENT_V2_API_KEY: str = config('EDOCUMENT_V2_API_KEY', cast=str)

# Dispensary
DISPENSARY_BASE_URL: str = config('DISPENSARY_BASE_URL', cast=str)
DISPENSARY_API_KEY: str = config('DISPENSARY_API_KEY', cast=str)

# Qamqor
QAMQOR_FACE_SEARCH_BASE_URL: str = config('QAMQOR_FACE_SEARCH_BASE_URL', cast=str)

# Address
ADDRESS_BASE_URL: str = config('ADDRESS_BASE_URL', cast=str)
ADDRESS_API_KEY: str = config('ADDRESS_API_KEY', cast=str)

# Personal Data
PERSONAL_ID_NUMBER: str = config('PERSONAL_ID_NUMBER', cast=str)
PHONE_NUMBER: str = config('PHONE_NUMBER', cast=str)
