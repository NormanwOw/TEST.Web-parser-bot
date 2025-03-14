import asyncio

from config import bot, dp
from src.infrastructure.logger.logger import Logger
from src.presentation.handlers.user_handlers import router as user_handlers_router
from src.presentation.callbacks.user_callbacks import router as user_callbacks_router


async def main():
    logger = Logger()
    logger.info('Start app...')
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        user_handlers_router,
        user_callbacks_router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
