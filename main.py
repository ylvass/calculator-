from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8895535615:AAEBzgkVzTGVUj9LAmHM8BItKBYHGHv7zgU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши две цены и количество.\n\n"
        "Пример:\n"
        "0.25 0.2 1000"
    )

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    try:
        parts = text.replace(",", ".").split()

        if len(parts) != 3:
            await update.message.reply_text("Нужно 3 числа:\nцена1 цена2 количество\n\nПример: 0.44 0.4 400")
            return

        price1 = float(parts[0])
        price2 = float(parts[1])
        amount = float(parts[2])

        # Меньшая цена → ЛОНГ, большая → ШОРТ
        if price1 <= price2:
            long_price = price1
            short_price = price2
        else:
            long_price = price2
            short_price = price1

        diff = short_price - long_price
        percent = (diff / long_price) * 100
        profit = diff * amount

        answer = (
            f"ЛОНГ: {long_price}\n"
            f"ШОРТ: {short_price}\n\n"
            f"Спред: {percent:.2f}%\n"
            f"Лавешка: {profit:.2f}$"
        )

        await update.message.reply_text(answer)

    except:
        await update.message.reply_text("Ошибка! Пример:\n0.44 0.4 400")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
