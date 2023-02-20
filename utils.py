from aiogram.dispatcher.filters.state import (StatesGroup,
                                              State)


class OrderStateGroup(StatesGroup):
    new_order = State()
    answer = State()
    secretkey = State()
    clarification = State()
    comment_to = State()
