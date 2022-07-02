from aiogram import Bot
from aiogram import Dispatcher

from bin_bot import bin_bot
from config import TOKEN
from config import FILE_NAME
from loader import get_first_four_curr


def main():
    print('Start program...')
    bn_bot = Bot(TOKEN)
    dp = Dispatcher(bn_bot)
    currencies_buttons = get_first_four_curr(FILE_NAME)
    currencies_buttons.append('FROM FILE')
    bin_bot(dp, currencies_buttons)


if __name__ == '__main__':
    main()


