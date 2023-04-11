import json

from aiogram import F, Router, types
from aiogram.filters import Command

from src.db_client.services import aggregate_payments


handlers_router = Router()
valid_query_example = '{"dt_from": "2022-09-01T00:00:00", "dt_upto": ' \
                      '"2022-12-31T23:59:00", "group_type": "month"}'


@handlers_router.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer("Hi! I'm PaymentAggregator!\n"
                         "For more information use /help\n"
                         "You may check connection to db with command /check")


@handlers_router.message(Command(commands=["help"]))
async def send_instruction(message: types.Message):
    await message.answer("<INSTRUCTION>")


@handlers_router.message(Command(commands=["check"]))
async def check_db_connection(message: types.Message):
    # Add some check
    await message.answer("Connection to DB: OK")


@handlers_router.message(F.text)
async def send_aggregated_payments(message: types.Message):
    query = json.loads(message.text)
    dt_from = query["dt_from"]
    dt_upto = query["dt_upto"]
    group_type = query["group_type"]
    payments = aggregate_payments(dt_from, dt_upto, group_type)
    await message.answer(payments)


@handlers_router.message()
async def get_wrong_type_message(message: types.Message):
    await message.answer("Invalid query. Use /help for instruction.")
