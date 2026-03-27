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
AKTIF_GRUPLAR = {} # {chat_id: True/False}
SPAM_HIZI = 0.5 

# --- HARMANLANMIŞ DEV KÜFÜR ARŞİVİ ---
sozler = [
    "ananın o süzme amcığını ranzayla beraber sikeyim", "kxrem senin o süzme orospu anneni sike sike dilsiz bıraksın",
    "hasret ananın amına tazyikli su sıkıp silsilece siktirsin", "yiğit babanın o kambur sırtında dölüyle resim yapsın",
    "şahabettin ananın amına jeneratör sokup tüm sülaleni siktirsin", "qq ananı pavyon köşelerinde sermaye yapıp kemiklerini kırsın",
    "ananın amına tır dorsesi sokup park edeyim ucube evladı", "kxrem bacının o daracık amcığını sike sike patlatsın",
    "hasret sülalendeki tüm kadınları ahıra kapatıp sike sike delirsin", "yiğit o ucube ananı kölem yapıp kırbaçla siktirsin",
    "şahabettin babanın kasketine boşalıp ananın kafasından aşağı döksün", "qq senin o fakir ve ezik ruhunu sülalenle beraber sikeyim",
    "kxrem annenle grup yaparken babana da kamerayı tuttursun", "hasret ananın o süzme amcığına beton mikseriyle girsin",
    "yiğit senin o beyinsiz kafatasını sike sike dağıtsın", "şahabettin ananın amına elektrik direği dikip trafo gibi kullansın",
    "qq senin o ucube gen haritanı sikeyim orospu artığı", "kxrem ananın amına asansör kurup her katta ayrı siktirsin",
    "hasret babanın mezarındaki toprakları sike sike çamur etsin", "yiğit bacını otobanda tır şoförlerine meze yapsın",
    "şahabettin sülaleni mezarlıkta sıraya dizip silsilece siktirsin", "qq ananın o buruşmuş amcığını jiletle kesip tuz bassın",
    "kxrem senin o ucube babanın kel kafasına döl fışkırtsın", "hasret ananı 7 kule zindanlarına atıp sike sike köle etsin",
    "yiğit bacının amına bayrak direği sokup dalgalandırsın", "şahabettin ananın amına yangın tüpü boşaltıp söndürsün",
    "qq senin doğduğun günü sülaleni geçmişini geleceğini sikeyim", "ananın amına inşaat iskelesi kurup 40 ameleyle sikeyim",
    "kxrem ananın amına matkapla girip delik deşik etsin", "hasret bacını kurban bayramında koç niyetine siktirsin",
    "yiğit senin o fakir babanın kamburunu dölüyle düzeltsin", "şahabettin ananın amına asansör kurup 10 kişiyle çıksın",
    "qq senin o köylü sülaleni şehrin ortasında sike sike inletsin", "ananın amına vapur yanaştırıp liman yapayım orospu dölü",
    "babanın tabutunu sikeyim ucube evladı mezarını sikeyim", "ananın amına kanca atıp denizde sikeyim balıklara yedireyim",
    "bacını pavyonda şampanya niyetine patlatayım", "kxrem senin o ucube sülaleni her gece kabusa çevirsin",
    "hasret ananın amına nükleer bomba atıp patlatsın", "yiğit bacını otogarda tır şoförlerine sermaye etsin",
    "şahabettin ananın o kara amcığını sike sike beyazlatsın", "qq senin o ucube hayatını sikeyim siktir git geber",
    "ananın amına mikserle girip ayran yapayım babana içireyim", "kxrem senin o ucube genlerini sike sike düzeltsin",
    "hasret bacının amcığını testereyle biçip silsilece siktirsin", "yiğit ananı her gece başka bir pavyonun önüne bağlasın",
    "şahabettin sülalendeki tüm kadınları köle pazarına satsın", "qq senin o süzme babanın mezarını dölle sulasın",
    "ananın amına kalorifer peteği sokup kışın ısınayım", "kxrem bacını sike sike dilsiz bırakıp kölesi yapsın",
    "hasret ananın amına tır makası sokup her gece inletsin", "yiğit senin o ucube varlığını yerle bir edip silsileni silsin",
    "şahabettin ananın amına dinamit döşeyip havaya uçursun", "qq senin o fakir ve zavallı onurunu sikeyim",
    "ananın amına beton mikseriyle girip anıt mezar yapayım", "kxrem sülalendeki her kadını sike sike delirsin",
    "hasret babanın kel kafasında dölüyle perküsyon çalsın", "yiğit ananın amına tünel açıp içinden metro geçirsin",
    "şahabettin bacının o dar amcığını sike sike mühürlesin", "qq senin doğduğun hastanenin başhekimini sikeyim",
    "ananın amına jeneratör sokup mahalleye elektrik vereyim", "kxrem sülalendeki tüm bakireleri sıraya dizip siktirsin",
    "hasret ananın o buruşmuş amcığını jiletle kesip tuz bassın", "yiğit senin o ucube babanın kamburunu dölüyle düzeltsin",
    "şahabettin ananın amına asansör kurup her katta ayrı siktirsin", "qq senin o fakir sülaleni sike sike zengin edeyim"
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
    if update.effective_user.id != OWNER_ID: return
    target = context.args[0] if context.args else "Hedef"
    HEDEFLER[target] = {"last_msg_id": None, "name": target}
    await context.bot.send_message(chat_id=OWNER_ID, text=f"🎯 Hedef eklendi: {target}")

async def bulk_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    for t in context.args:
        HEDEFLER[t] = {"last_msg_id": None, "name": t}
    await context.bot.send_message(chat_id=OWNER_ID, text=f"💣 {len(context.args)} kişi listeye alındı.")

async def baslat_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    # Eğer argüman varsa (kullanıcı adı), onu kullan; yoksa içinde bulunulan grubu kullan
    grup_id = context.args[0] if context.args else update.effective_chat.id
    
    AKTIF_GRUPLAR[str(grup_id)] = True
    await context.bot.send_message(chat_id=OWNER_ID, text=f"🚀 {grup_id} grubunda AV BAŞLADI.")
    
    while AKTIF_GRUPLAR.get(str(grup_id), False):
        for t_id, data in list(HEDEFLER.items()):
            if not AKTIF_GRUPLAR.get(str(grup_id), False): break
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

async def dur_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    
    # 1. Senaryo: DM'den /dur @grupismi yazmak
    if context.args:
        target_chat = context.args[0]
        AKTIF_GRUPLAR[str(target_chat)] = False
        await context.bot.send_message(chat_id=OWNER_ID, text=f"🛑 {target_chat} durduruldu.")
    
    # 2. Senaryo: Grubun içinde direkt /dur yazmak (Özellikle gizli gruplar için)
    else:
        current_chat = str(update.effective_chat.id)
        if current_chat in AKTIF_GRUPLAR:
            AKTIF_GRUPLAR[current_chat] = False
            # Grup içinde iz bırakmamak için onay mesajını yine DM'den atar
            await context.bot.send_message(chat_id=OWNER_ID, text=f"🛑 Gizli gruptaki ({current_chat}) saldırı sonlandırıldı.")

async def sleep_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SPAM_HIZI
    if update.effective_user.id == OWNER_ID and context.args:
        SPAM_HIZI = float(context.args[0])
        await context.bot.send_message(chat_id=OWNER_ID, text=f"⏱ Hız: {SPAM_HIZI}s")

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
