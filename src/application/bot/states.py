from aiogram.fsm.state import StatesGroup, State


class FileStates(StatesGroup):
    get_file = State()