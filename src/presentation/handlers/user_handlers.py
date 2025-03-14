from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.application.bot.keyboards.inline import cancel_kb
from src.application.bot.keyboards.reply import main_kb
from src.application.bot.messages import START_MESSAGE, INCORRECT_FILE_STRUCTURE, UNKNOWN_EX, FILE_NAME_EX
from src.application.bot.states import FileStates
from src.application.exceptions import FileStructureException, FileNameException
from src.application.use_cases.collect_products_use_case import CollectProductsUseCase
from src.application.use_cases.handle_file_use_case import HandleFileUseCase
from src.domain.entities import File, Product, Query
from src.domain.services.file_parser_service import PandasFileParser
from src.domain.services.web_parser_service import BSWebParser
from src.infrastructure.session import async_session
from src.infrastructure.uow.impl import UnitOfWork
from src.infrastructure.logger import logger

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.clear()
    await message.answer(text=START_MESSAGE, reply_markup=main_kb())


@router.message(F.text == '📥 Загрузить файл')
async def set_state_file_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Загрузите файл в формате *.xlsx:', reply_markup=cancel_kb())
    await state.set_state(FileStates.get_file)


@router.message(FileStates.get_file, F.document)
async def file_handler(message: types.Message, state: FSMContext, bot: Bot):
    try:
        doc = message.document
        file = File(
            id=doc.file_id,
            name=doc.file_name,
            user_id=message.from_user.id
        )
        file_parser = PandasFileParser(logger)
        uow = UnitOfWork(async_session)
        handle_file = HandleFileUseCase(bot, file_parser, uow, logger)

        queries_from_file = await handle_file(file)
        await Query.send_message_with_queries(queries_from_file, bot, message.from_user.id)
        await state.clear()
        await Query.send_message_with_start_parser(queries_from_file, bot, message.from_user.id)

        for query in queries_from_file:
            web_parser = BSWebParser(
                url=query.url,
                xpath=query.xpath,
                next_page_xpath=query.next_page_xpath,
                logger=logger
            )
            collect_products = CollectProductsUseCase(web_parser, logger)
            products = await collect_products()
            await message.answer(
                f'<b>Найдено {len(products)} товаров на сайте</b> {query.url}\n'
                f'<b>Средняя стоимость</b>: {Product.get_avg_price(products)}' + products[0].currency
            )
    except FileNameException:
        await message.answer(FILE_NAME_EX)
    except FileStructureException:
        await message.answer(INCORRECT_FILE_STRUCTURE)
    except Exception:
        await message.answer(UNKNOWN_EX)
        logger.error('Ошибка в file_handler', exc_info=True)

    await state.clear()
