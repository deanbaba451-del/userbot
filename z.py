import os, random, threading, uuid
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- AYARLAR ---
OWNER_ID = 6534222591
# GÜNCEL TOKEN
BOT_TOKEN = "8529963153:AAFMaps4J07prteWIn48HMGw3eBnXdCEPiE"
app = Flask(__name__)

# Alem Hasta Kemik Kadro
TAYFA = ["keyra", "hasret", "yiğit", "kerem", "şahabettin", "qq"]

user_data = {} 
promo_codes = {}

@app.route('/')
def health(): return "alem hasta aktif", 200

def get_user(uid, name):
    name_lower = str(name).lower()
    if uid not in user_data:
        # Kemik kadroya biraz daha yüksek başlangıç şansı
        start_size = random.randint(15, 25) if any(x in name_lower for x in TAYFA) else random.randint(10, 18)
        user_data[uid] = {"size": start_size, "name": name_lower}
    return user_data[uid]

# --- ANA KOMUTLAR ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🍆 ALEM HASTA KRALLIĞINA HOŞ GELDİN! 🍆\n\n"
        "Burası devasa malı olanların er meydanı! 🚀\n\n"
        "🔥 TAYFA BURADA MI?\n"
        "qq - keyra - hasret - yiğit - kerem - şahabettin\n\n"
        "📏 /uzat — Malına mal kat!\n"
        "🏆 /siralama — Kimin borusu ötüyor gör!\n"
        "🎲 /yt <miktar> — Yazı tura!\n"
        "🃏 /bk <miktar> — Bul karayı!\n"
        "🗣️ /diss — Tayfaya özel ayar!\n\n"
        "🌟 EMEĞİ GEÇENLER: @komtanim"
    )
    await update.message.reply_text(msg)

async def diss_at(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.reply_to_message.from_user.first_name.lower() if update.message.reply_to_message else "herkes"
    
    responses = [
        f"lan {target}, qq yapma sesini kes!",
        f"{target}, şahabettin bile senden daha delikanlı duruyor.",
        f"hasret gibi ağlama, oyununa bak {target}.",
        f"yiğit'in malı senden büyük, boşa kasma {target}.",
        "kerem'e sor bakalım, o da senin gibi boş mu yapıyordu?",
        "keyra görse haline güler, kapat konuyu.",
        "bu grupta sadece krallar konuşur, sen bekle."
    ]
    await update.message.reply_text(random.choice(responses))

async def uzat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid, update.effective_user.first_name)
    
    bonus = 2 if any(x in user["name"] for x in TAYFA) else 0
    change = random.randint(-5, 10) + bonus
    user["size"] += change
    if user["size"] < 1: user["size"] = 1
    
    text = f"📏 Sonuç: {'+' if change >= 0 else ''}{change} cm\n🍆 Yeni Boy: {user['size']} cm"
    if change < 0: text += "\n🥀 Hahaha! Bamya kadar kaldı elinde, yazık!"
    await update.message.reply_text(text)

async def siralama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data:
        return await update.message.reply_text("henüz kimse malını ölçmedi.")
    
    sort = sorted(user_data.items(), key=lambda x: x[1]['size'], reverse=True)[:10]
    txt = "🏆 ALEM HASTA EN BÜYÜK MAL SIRALAMASI 🏆\n\n"
    for i, (uid, data) in enumerate(sort, 1):
        crown = "👑" if i == 1 else "🔹"
        txt += f"{crown} {i}. {data['name']} — {data['size']} cm\n"
    await update.message.reply_text(txt)

# --- KUMARHANE ---

async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        bet = int(context.args[0])
        user = get_user(update.effective_user.id, update.effective_user.first_name)
        if bet > user["size"]: return await update.message.reply_text(f"❗ Yetersiz boy! Senin malın: {user['size']} cm")

        keyboard = [[InlineKeyboardButton("🟡 YAZI", callback_data=f"yt_y_{bet}"),
                     InlineKeyboardButton("🦅 TURA", callback_data=f"yt_t_{bet}")]]
        await update.message.reply_text(f"🎲 BAHİS BAŞLADI!\nBahis: {bet} cm\nSeçimini yap:", reply_markup=InlineKeyboardMarkup(keyboard))
    except: await update.message.reply_text("Kullanım: /yt <miktar>")

async def bk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        bet = int(context.args[0])
        user = get_user(update.effective_user.id, update.effective_user.first_name)
        if bet > user["size"]: return await update.message.reply_text("❗ Yetersiz boy!")

        keyboard = [[InlineKeyboardButton("🥤 1", callback_data=f"bk_1_{bet}"),
                     InlineKeyboardButton("🥤 2", callback_data=f"bk_2_{bet}"),
                     InlineKeyboardButton("🥤 3", callback_data=f"bk_3_{bet}")]]
        await update.message.reply_text(f"🃏 BUL KARAYI AL PARAYI!\nBahis: {bet} cm", reply_markup=InlineKeyboardMarkup(keyboard))
    except: pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split("_")
    user = get_user(query.from_user.id, query.from_user.first_name)
    bet = int(data[2])

    if data[0] == "yt":
        win = random.choice(["y", "t"])
        if data[1] == win:
            user["size"] += bet
            await query.edit_message_text(f"🎉 KAZANDIN!\nÖdül: +{bet} cm\nYeni Boy: {user['size']} cm 🚀")
        else:
            user["size"] -= bet
            await query.edit_message_text(f"💀 KAYBETTİN!\nGiden: -{bet} cm\nYeni Boy: {user['size']} cm 🥀")

    if data[0] == "bk":
        correct = str(random.randint(1, 3))
        if data[1] == correct:
            user["size"] += bet * 2
            await query.edit_message_text(f"✅ DOĞRU BARDAK!\nÖdül: +{bet*2} cm\nYeni Boy: {user['size']} cm 🔥")
        else:
            user["size"] -= bet
            await query.edit_message_text(f"❌ YANLIŞ! Kara {correct}. bardaktaydı.\nYeni Boy: {user['size']} cm\nBamya kadar kaldı elinde!")

# --- ADMIN ---
async def promokodolustur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    code = str(uuid.uuid4())[:6].upper()
    val = random.randint(20, 50)
    promo_codes[code] = val
    await update.message.reply_text(f"🎫 Kod: {code}\nDeğer: {val} cm")

def main():
    bot = Application.builder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("uzat", uzat))
    bot.add_handler(CommandHandler("siralama", siralama))
    bot.add_handler(CommandHandler("yt", yt))
    bot.add_handler(CommandHandler("bk", bk))
    bot.add_handler(CommandHandler("diss", diss_at))
    bot.add_handler(CommandHandler("promokodolustur", promokodolustur))
    bot.add_handler(CallbackQueryHandler(button_handler))

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    bot.run_polling()

if __name__ == "__main__":
    main()
