import datetime
import json

from aiogram import F, Router, types
from aiogram.filters import Command

from src.db_client.services import aggregate_payments, get_date_range


handlers_router = Router()
valid_query_example = '{"dt_from": "2022-09-01T00:00:00", "dt_upto": ' \
                      '"2022-12-31T23:59:00", "group_type": "month"}'
invalid_query_message = "Invalid message format. Example of query:\n\n" \
                        f"{valid_query_example}\n\n" \
                        "For more information use /help"
instruction = f"""Send a JSON string containing the following fields:
"dt_from" - date and time of aggregation start in ISO format;
"dt_upto" - date and time of aggregation finish in ISO format;
"group_type" - type of aggregation, can be "hour", "day" or "month".

Example of query:
{valid_query_example}"""


@handlers_router.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer("Hi! I'm PaymentAggregator!\n"
                         "For more information use /help\n"
                         "You may check connection to db with command /check")


@handlers_router.message(Command(commands=["help"]))
async def send_instruction(message: types.Message):
    await message.answer(instruction)


@handlers_router.message(Command(commands=["check"]))
async def check_db_connection(message: types.Message):
    try:
        min_date, max_date = await get_date_range()
    except Exception:
        await message.answer("Connection to DB: FAIL.")
    else:
        await message.answer("Connection to DB: OK.\n"
                             f"Available date range: {min_date} - {max_date}")


@handlers_router.message(F.text)
async def send_aggregated_payments(message: types.Message):
    try:
        query = json.loads(message.text)
        dt_from = datetime.datetime.fromisoformat(query["dt_from"])
        dt_upto = datetime.datetime.fromisoformat(query["dt_upto"])
        group_type = query["group_type"]
    except Exception:
        await message.answer(invalid_query_message)
    else:
        if group_type in ["month", "day", "hour"]:
            payments = await aggregate_payments(dt_from, dt_upto, group_type)
            await message.answer(payments)
        else:
            await message.answer(invalid_query_message)


@handlers_router.message()
async def get_wrong_type_message(message: types.Message):
    await message.answer(invalid_query_message)
