from redis.asyncio import Redis
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from app.service.healthchecker import healthchecker
from settings.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
)

cross_emoji = u'\u274C'
tick_emoji = u'\u2705'
status_emojis = [cross_emoji, tick_emoji]

router = Router()
redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
)


@router.message(Command('start'))
async def start_handler(message: Message):
    await redis.sadd(
        'chat_ids',
        str(message.chat.id),
    )
    await message.answer('Hello! I am Biometric Healthcheck Service Bot!')


@router.message(Command('stop'))
async def start_handler(message: Message):
    await redis.srem(
        'chat_ids',
        str(message.chat.id),
    )
    await message.answer('Thank you for using service of Biometric Healthcheck Service Bot!')


def create_healthcheck_message(
    **kwargs
):
    message = "Statuses of Biometric Service:\n"
    message += f"Liveness: {status_emojis[kwargs.get('is_liveness_healthy')]}\n"
    message += f"Face2Face: {status_emojis[kwargs.get('is_face2face_healthy')]}\n"
    message += f"DocRecognition: {status_emojis[kwargs.get('is_doc_recognition_healthy')]}\n"
    message += f"EDocument: {status_emojis[kwargs.get('is_edocument_healthy')]}\n"
    message += f"Addresses: {status_emojis[kwargs.get('is_addresses_healthy')]}\n"
    message += f"Dispensary: {status_emojis[kwargs.get('is_dispensary_healthy')]}\n"
    message += f"Qamqor FS: {status_emojis[kwargs.get('is_qamqor_healthy')]}"
    return message


@router.message(Command('check'))
async def check_handler(message: Message):
    results = healthchecker.get_status()
    healthcheck_message = create_healthcheck_message(**results)
    await message.answer(healthcheck_message)


async def send_statuses_message(
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
