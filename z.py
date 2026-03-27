import os
import asyncio
import threading
import random
import string
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

app = Flask('')

@app.route('/')
def home(): return "Bot Aktif"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- AYARLAR ---
TOKEN = "8685088803:AAGomXnBLdQ-ZRz8Mzssl9dS7d_FlKU6zFY"
OWNER_ID = 6534222591
HEDEFLER = {} 
SALDIRI_DURUMU = False
SPAM_HIZI = 0.6 

sozler = [
    "ananın o süzme amcığını ranzayla beraber sikeyim", "emekli babanın o titrek ellerini dölümle yıkayayım",
    "bacının amcığına beton döküp üzerinde heykelini sikeyim", "ananın amına nükleer santral kurup mahallece boşalalım",
    "seni doğuran o ebenin parmaklarını sike sike koparayım", "ananın amına tır dorsesi sokup park edeyim ucube evladı",
    "babanın o çürümüş mezarını sike sike deşeyim orospu artığı", "ananın amında saltanat kurar hüküm sürerim",
    "regl ananın kanını babana şarap niyetine içireyim ucube", "bacını kurban pazarında siktire siktire öldüreyim",
    "ananın amına kepçe sokup kanalizasyon açayım", "o ucube sülaleni mezarlıkta sıraya dizip sikeyim",
    "ananı her gece başka mahallede siktireyim orospu dölü", "babanın o amele suratına tazyikli boşalayım",
    "ananın amına asansör kurup kat kat sikeyim ucube evladı", "senin varlığını galaksiden kazıyıp sikeyim",
    "ananın amına foseptik çukuru açıp içine boşalayım", "bacının o ucube amcığını testereyle kesip sikeyim",
    "ananın amında mangal yapıp babana yedireyim orospu çocuğu", "seni doğuran o ananın amcığını mühürleyeyim",
    "kxrem senin o süzme orospu anneni sike sike dilsiz bıraksın",
    "hasret ananın amına tazyikli su sıkıp silsilece siktirsin",
    "yiğit babanın o kambur sırtında dölüyle resim yapsın ucube evladı",
    "şahabettin ananın amına jeneratör sokup tüm sülaleni siktirsin",
    "qq ananı pavyon köşelerinde sermaye yapıp kemiklerini kırsın",
    "kxrem bacının o daracık amcığını sike sike patlatsın",
    "hasret sülalendeki tüm kadınları ahıra kapatıp sike sike delirsin",
    "yiğit o ucube ananı kölem yapıp kırbaçla siktirsin",
    "şahabettin babanın kasketine boşalıp ananın kafasından aşağı döksün",
    "qq senin o fakir ve ezik ruhunu sülalenle beraber sikeyim",
    "kxrem annenle grup yaparken babana da kamerayı tuttursun",
    "hasret ananın o süzme amcığına beton mikseriyle girsin",
    "yiğit senin o beyinsiz kafatasını sike sike dağıtsın",
    "şahabettin ananın amına elektrik direği dikip trafo gibi kullansın",
    "qq senin o ucube gen haritanı sikeyim orospu artığı",
    "kxrem ananın amına asansör kurup her katta ayrı siktirsin",
    "hasret babanın mezarındaki toprakları sike sike çamur etsin",
    "yiğit bacını otobanda tır şoförlerine meze yapsın",
    "şahabettin sülaleni mezarlıkta sıraya dizip silsilece siktirsin",
    "qq ananın o buruşmuş amcığını jiletle kesip tuz bassın",
    "kxrem senin o ucube babanın kel kafasına döl fışkırtsın",
    "hasret ananı 7 kule zindanlarına atıp sike sike köle etsin",
    "yiğit bacının amına bayrak direği sokup dalgalandırsın",
    "şahabettin ananın amına yangın tüpü boşaltıp söndürsün",
    "qq senin doğduğun günü sülaleni geçmişini geleceğini sikeyim"
]

def anti_spam_text(text):
    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{text} 🔥 {random_str}"

async def monitor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user: return
    uid = str(update.message.from_user.id)
    uname = f"@{update.message.from_user.username}" if update.message.from_user.username else uid
    if uid in HEDEFLER or uname in HEDEFLER:
        key = uid if uid in HEDEFLER else uname
        HEDEFLER[key]["last_msg_id"] = update.message.message_id
        HEDEFLER[key]["name"] = update.message.from_user.first_name

async def ekle_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID or not context.args: return
    target = context.args[0]
    HEDEFLER[target] = {"last_msg_id": None, "name": target}
    await context.bot.send_message(chat_id=OWNER_ID, text=f"🎯 Hedef eklendi: {target}")

async def bulk_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    for t in context.args:
        HEDEFLER[t] = {"last_msg_id": None, "name": t}
    await context.bot.send_message(chat_id=OWNER_ID, text=f"💣 {len(context.args)} hedef listeye alındı.")

async def baslat_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SALDIRI_DURUMU
    if update.effective_user.id != OWNER_ID or not context.args: return
    grup_id = context.args[0]
    SALDIRI_DURUMU = True
    await context.bot.send_message(chat_id=OWNER_ID, text=f"🚀 {grup_id} üzerinde imha başladı.")
    
    while SALDIRI_DURUMU:
        for t_id, data in list(HEDEFLER.items()):
            if not SALDIRI_DURUMU: break
            try:
                soz = anti_spam_text(random.choice(sozler))
                msg_text = f"**{data['name'].upper()}** {soz}"
                if data["last_msg_id"]:
                    await context.bot.send_message(chat_id=grup_id, text=msg_text, reply_to_message_id=data["last_msg_id"], parse_mode="Markdown")
                else:
                    await context.bot.send_message(chat_id=grup_id, text=f"{t_id} {soz}", parse_mode="Markdown")
                await asyncio.sleep(SPAM_HIZI)
            except:
                await asyncio.sleep(1)

async def sleep_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SPAM_HIZI
    if update.effective_user.id == OWNER_ID and context.args:
        SPAM_HIZI = float(context.args[0])
        await context.bot.send_message(chat_id=OWNER_ID, text=f"⏱ Yeni hız: {SPAM_HIZI}s")

async def dur_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SALDIRI_DURUMU
    if update.effective_user.id == OWNER_ID:
        SALDIRI_DURUMU = False
        HEDEFLER.clear()
        await context.bot.send_message(chat_id=OWNER_ID, text="🛑 OPERASYON DURDURULDU VE TEMİZLENDİ.")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("ekle", ekle_komutu))
    app_bot.add_handler(CommandHandler("bulk", bulk_komutu))
    app_bot.add_handler(CommandHandler("baslat", baslat_komutu))
    app_bot.add_handler(CommandHandler("dur", dur_komutu))
    app_bot.add_handler(CommandHandler("sleep", sleep_komutu))
    app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND, monitor_handler))
    app_bot.run_polling()
