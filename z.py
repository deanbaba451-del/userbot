import os
import asyncio
import threading
import random
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# render.com ayarı
app = Flask('')

@app.route('/')
def home():
    return "bot aktif"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- AYARLAR ---
TOKEN = "8685088803:AAGpy_NoEUd4dRWgc2YHTEkTdsfD2XYYNTA"
OWNER_ID = 6534222591
HEDEFLER = set()

# botun söyleyeceği mesajlar buraya (istediğin kadar ekle)
sozler = [
    "sustun",
    "yazma artik",
    "ses ver",
    "bekliyorum",
    "tmm",
    "yaz yaz",
    "ne oldu"
]

async def target_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        try:
            yeni_id = int(context.args[0].strip())
            HEDEFLER.add(yeni_id)
            await update.message.reply_text(f"{yeni_id} listeye eklendi")
        except:
            pass

async def bulk_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        raw_input = " ".join(context.args)
        raw_ids = raw_input.split(",")
        for r_id in raw_ids:
            clean_id = r_id.strip()
            if clean_id.isdigit():
                HEDEFLER.add(int(clean_id))
        await update.message.reply_text("idler eklendi")

async def tetikleyici(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    msg_id = update.message.message_id
    text = update.message.text

    # durdurma kontrolü (owner .h yazınca)
    if text.lower() == ".h" and user_id == OWNER_ID:
        HEDEFLER.clear()
        await context.bot.send_message(chat_id=chat_id, text="tmm", reply_to_message_id=msg_id)
        return

    # hedef listede mi kontrol et
    if user_id in HEDEFLER:
        # owner durdurana kadar döngü başlar
        while user_id in HEDEFLER:
            try:
                # listeden rastgele bir söz seçer
                cevap = random.choice(sozler)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=cevap,
                    reply_to_message_id=msg_id
                )
                await asyncio.sleep(2) # 2 saniyede bir atar
            except:
                break

if __name__ == '__main__':
    # flask başlat
    threading.Thread(target=run_flask, daemon=True).start()

    # bot başlat
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("target", target_ekle))
    app_bot.add_handler(CommandHandler("bulk", bulk_ekle))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), tetikleyici))

    app_bot.run_polling()
