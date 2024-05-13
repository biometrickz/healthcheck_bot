import asyncio
import logging

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.fsm.storage.memory import (
    MemoryStorage,
)

from settings.config import (
    TOKEN,
)
from app.service.healthchecker import healthchecker
from app.handlers.messages import (
    router,
    send_statuses_message,
)

bot = Bot(token=TOKEN)


async def start_bot():
    logging.info('Starting telegram bot...')
    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    dp.include_router(router=router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


async def start_healthcheck():
    logging.info('Starting healthcheck...')
    while True:
        await healthchecker.check_all()
        statuses = healthchecker.get_status_values()

        if not all(statuses):
            await send_statuses_message(
                bot=bot,
                **healthchecker.get_statuses(),
                **healthchecker.get_codes(),
            )
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(30)


async def main():
    await asyncio.gather(
        start_bot(),
        start_healthcheck(),
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
