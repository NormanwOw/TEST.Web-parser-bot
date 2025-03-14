from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data == 'cancel')
async def cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Ввод отменён', show_alert=True)
    await callback.message.delete()