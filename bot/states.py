from aiogram.fsm.state import State, StatesGroup

class AddChannel(StatesGroup):
    waiting_chat_id = State()
    waiting_price = State()
    waiting_period = State()
