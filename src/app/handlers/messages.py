from redis.asyncio import Redis
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from app.service.healthchecker import (
    healthchecker,
)
from settings.config import (
    REDIS_HOST,
    REDIS_HOST_PORT,
    REDIS_DB,
)

status_emojis = ['❌', '✅']

router = Router()
redis = Redis(
    host=REDIS_HOST,
    port=REDIS_HOST_PORT,
    db=REDIS_DB,
)


@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    await redis.sadd(
        'chat_ids',
        str(message.chat.id),
    )
    await message.answer('Hello! I am Biometric Healthcheck Service Bot!')


@router.message(Command('stop'))
async def start_handler(message: Message) -> None:
    await redis.srem(
        'chat_ids',
        str(message.chat.id),
    )
    await message.answer('Thank you for using service of Biometric Healthcheck Service Bot!')


def create_healthcheck_message(
    **kwargs
) -> str:
    message = "Statuses of Biometric Services:\n"
    message += (f"Liveness: {status_emojis[kwargs.get('is_liveness_healthy')]} | "
                f"code: {kwargs.get('liveness_code')}\n")
    message += (f"Face2Face: {status_emojis[kwargs.get('is_face2face_healthy')]} | "
                f"code: {kwargs.get('face2face_code')}\n")
    message += (f"DocRecognition: {status_emojis[kwargs.get('is_doc_recognition_healthy')]} | "
                f"code: {kwargs.get('doc_recognition_code')}\n")
    message += (f"EDocument: {status_emojis[kwargs.get('is_edocument_healthy')]} | "
                f"code: {kwargs.get('edocument_code')}\n")
    message += (f"Addresses: {status_emojis[kwargs.get('is_addresses_healthy')]} | "
                f"code: {kwargs.get('addresses_code')}\n")
    message += (f"Dispensary: {status_emojis[kwargs.get('is_dispensary_healthy')]} | "
                f"code: {kwargs.get('dispensary_code')}\n")
    message += (f"Qamqor FS: {status_emojis[kwargs.get('is_qamqor_healthy')]} | "
                f"code: {kwargs.get('qamqor_code')}")
    return message


@router.message(Command('check'))
async def check_handler(message: Message) -> None:
    statuses = healthchecker.get_statuses()
    codes = healthchecker.get_codes()
    healthcheck_message = create_healthcheck_message(**statuses, **codes)
    await message.answer(healthcheck_message)


async def send_statuses_message(
    *,
    bot: Bot,
    **kwargs
):
    healthcheck_message = create_healthcheck_message(**kwargs)
    chat_ids = await redis.smembers('chat_ids')
    if chat_ids:
        for chat_id in chat_ids:
            await bot.send_message(
                chat_id=chat_id.decode('ascii'),
                text=healthcheck_message,
            )
