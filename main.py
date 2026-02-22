import asyncio
import logging
from datetime import datetime, timedelta, timezone



from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.enums import ContentType

BOT_TOKEN = "7729444914:AAGdmkSMrr2SH0pVzej1ERRDTqGmbIaUh6k"
PAYMENT_PROVIDER_TOKEN = "381764678:TEST:380f3c9b-1e5c-4a7d-8b0e-9c8a1b2c3d4e"  # Замените на ваш PAYMENT_PROVIDER_TOKEN
GROUP_ID = -1001234567890  # Замените на ваш GROUP_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ==========================
# Проверка GROUP_ID
# ==========================
@dp.message(Command("getid"))
async def get_id(message: Message):
    await message.answer(f"Chat ID: {message.chat.id}")
    print("Debug: chat.id =", message.chat.id)

# ==========================
# Старт и команда покупки
# ==========================
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Здравствуй! Чтобы получить доступ к закрытой группе, напишите на данный номер +77084828870, цена доступа 5000 KZT. После оплаты вы получите ссылку на группу. Дальнейшие инструкции будут в чате.")


@dp.message(Command("buy"))
async def buy(message: Message):
    prices = [LabeledPrice(label="Group Access", amount=500000)]  # 5000 KZT
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Закрытая группа",
        description="Одноразовый доступ",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="KZT",
        prices=prices,
        start_parameter="group-access",
        payload=f"group-access-{message.from_user.id}",
    )


# ==========================
# Предварительная проверка платежа
# ==========================
@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# ==========================
# Успешная оплата + invite link
# ==========================
@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    # Ссылка действительна 10 минут, одноразовая
    expire = datetime.now(timezone.utc) + timedelta(minutes=100)

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=GROUP_ID,
            member_limit=1,
            expire_date=expire
        )
    except Exception as e:
        await message.answer(f"Ошибка при создании ссылки: {e}")
        logging.error("Invite link error", exc_info=e)
        return

    await message.answer(
        "Оплата прошла успешно ✅\n\n"
        "Вот ваша ссылка (действует 10 минут):\n\n"
        f"{invite_link.invite_link}"
    )


# ==========================
# Основной цикл бота
# ==========================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())