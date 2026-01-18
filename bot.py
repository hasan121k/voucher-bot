import telebot, time, threading
from config import BOT_TOKEN
from database import *
from security import encrypted_password

bot = telebot.TeleBot(BOT_TOKEN)

def joined(channel, uid):
    try:
        return bot.get_chat_member(
            channel, uid
        ).status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m, "🎟️ Voucher code পাঠাও")

@bot.message_handler(func=lambda m: m.text.isdigit())
def redeem(m):
    uid = m.from_user.id
    code = m.text.strip()

    v = get_voucher(code)
    if not v:
        return bot.reply_to(m, "❌ Invalid voucher")
    if v[4] == 0:
        return bot.reply_to(m, "🚫 Disabled voucher")
    if v[5] == 1:
        return bot.reply_to(m, "⏸️ Voucher paused")
    if v[1] < int(time.time()):
        return bot.reply_to(m, "⏳ Voucher expired")
    if v[3] >= v[2]:
        return bot.reply_to(m, "❌ Limit finished")

    channel = get_setting("channel")
    if channel and not joined(channel, uid):
        return bot.reply_to(m, f"📢 Join channel first:\n{channel}")

    use_voucher(uid, code)

    bot.reply_to(
        m,
        f"✅ Password:\n`{encrypted_password()}`",
        parse_mode="Markdown"
    )

threading.Thread(target=lambda: bot.infinity_polling()).start()
