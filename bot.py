from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8772735079:AAEuEYw1DTrar2rJnB4XQZp4wpzN1EfIiVs"
ADMIN_ID = 2083913926

# منوی اصلی
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📦 خرید پلن", callback_data="buy")],
        [InlineKeyboardButton("📩 پشتیبانی", url="https://t.me/yourid")]
    ]
    return InlineKeyboardMarkup(keyboard)

# منوی پلن‌ها
def plan_menu():
    keyboard = [
        [InlineKeyboardButton("1 گیگ ماهانه - 350 تومن", callback_data="plan1")],
        [InlineKeyboardButton("50 مگ تست - 45 تومن", callback_data="test")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 به ربات فروش VPN خوش اومدی",
        reply_markup=main_menu()
    )

# callback ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.message.edit_text("📦 یکی از پلن‌ها رو انتخاب کن:", reply_markup=plan_menu())

    elif query.data == "plan1":
        context.user_data["plan"] = "1 گیگ ماهانه"
        await query.message.edit_text(
            "📦 پلن: 1 گیگ ماهانه\n💰 قیمت: 350,000 تومان\n\n💳 پرداخت:\n1234 5678 9012 3456\n\n📸 بعد از واریز رسید رو بفرست"
        )

    elif query.data == "test":
        context.user_data["plan"] = "50 مگ تست"
        await query.message.edit_text(
            "📦 پلن تست: 50 مگابایت\n💰 قیمت: 45,000 تومان\n\n💳 پرداخت:\n1234 5678 9012 3456\n\n📸 بعد از واریز رسید رو بفرست"
        )

    elif query.data == "back":
        await query.message.edit_text("🏠 منوی اصلی:", reply_markup=main_menu())

# گرفتن عکس رسید
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    plan = context.user_data.get("plan", "نامشخص")

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"📥 رسید جدید\n\n👤 کاربر: {user.id}\n📦 پلن: {plan}"
    )

    await update.message.reply_text("✅ رسید ارسال شد، منتظر تایید باش")

# run
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
