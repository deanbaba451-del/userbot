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
SPAM_HIZI = 0.5 

# --- DEV HARMANLANMIŞ KÜFÜR ARŞİVİ (2 KAT GÜÇLENDİRİLDİ) ---
sozler = [
    "ananın o süzme amcığını ranzayla beraber sikeyim", 
    "kxrem senin o süzme orospu anneni sike sike dilsiz bıraksın",
    "emekli babanın o titrek ellerini dölümle yıkayayım",
    "hasret ananın amına tazyikli su sıkıp silsilece siktirsin",
    "bacının amcığına beton döküp üzerinde heykelini sikeyim", 
    "yiğit babanın o kambur sırtında dölüyle resim yapsın",
    "ananın amına nükleer santral kurup mahallece boşalalım",
    "şahabettin ananın amına jeneratör sokup tüm sülaleni siktirsin",
    "seni doğuran o ebenin parmaklarını sike sike koparayım", 
    "qq ananı pavyon köşelerinde sermaye yapıp kemiklerini kırsın",
    "ananın amına tır dorsesi sokup park edeyim ucube evladı", 
    "kxrem bacının o daracık amcığını sike sike patlatsın",
    "babanın o çürümüş mezarını sike sike deşeyim orospu artığı", 
    "hasret sülalendeki tüm kadınları ahıra kapatıp sike sike delirsin",
    "ananın amında saltanat kurar hüküm sürerim",
    "yiğit o ucube ananı kölem yapıp kırbaçla siktirsin",
    "regl ananın kanını babana şarap niyetine içireyim ucube", 
    "şahabettin babanın kasketine boşalıp ananın kafasından aşağı döksün",
    "bacını kurban pazarında siktire siktire öldüreyim",
    "qq senin o fakir ve ezik ruhunu sülalenle beraber sikeyim",
    "ananın amına kepçe sokup kanalizasyon açayım", 
    "kxrem annenle grup yaparken babana da kamerayı tuttursun",
    "o ucube sülaleni mezarlıkta sıraya dizip sikeyim",
    "hasret ananın o süzme amcığına beton mikseriyle girsin",
    "ananı her gece başka mahallede siktireyim orospu dölü", 
    "yiğit senin o beyinsiz kafatasını sike sike dağıtsın",
    "babanın o amele suratına tazyikli boşalayım",
    "şahabettin ananın amına elektrik direği dikip trafo gibi kullansın",
    "ananın amına asansör kurup kat kat sikeyim ucube evladı", 
    "qq senin o ucube gen haritanı sikeyim orospu artığı",
    "senin varlığını galaksiden kazıyıp sikeyim",
    "kxrem ananın amına asansör kurup her katta ayrı siktirsin",
    "ananın amına foseptik çukuru açıp içine boşalayım", 
    "hasret babanın mezarındaki toprakları sike sike çamur etsin",
    "bacının o ucube amcığını testereyle kesip sikeyim",
    "yiğit bacını otobanda tır şoförlerine meze yapsın",
    "ananın amında mangal yapıp babana yedireyim orospu çocuğu", 
    "şahabettin sülaleni mezarlıkta sıraya dizip silsilece siktirsin",
    "seni doğuran o ananın amcığını sikeyim",
    "qq ananın o buruşmuş amcığını jiletle kesip tuz bassın",
    "ananın amına tazyikli su sıkıp temizledikten sonra silsilece siktireyim", 
    "kxrem senin o ucube babanın kel kafasına döl fışkırtsın",
    "babanın o kambur sırtında dölümle resim yapayım ucube",
    "hasret ananı 7 kule zindanlarına atıp sike sike köle etsin",
    "ananın amına elektrik direği dikip trafo gibi kullanayım", 
    "yiğit bacının amına bayrak direği sokup dalgalandırsın",
    "senin o beyinsiz kafatasını sike sike dağıtayım",
    "şahabettin ananın amına yangın tüpü boşaltıp söndürsün",
    "ananın amına jeneratör sokup elektrik üreterek tüm sülaleni sikeyim", 
    "qq senin doğduğun günü sülaleni geçmişini geleceğini sikeyim",
    # --- YENİ EKLENEN 2. KAT KÜFÜRLER ---
    "ananın amına inşaat iskelesi kurup 40 ameleyle sikeyim",
    "kxrem ananın amına matkapla girip delik deşik etsin",
    "hasret bacını kurban bayramında koç niyetine siktirsin",
    "yiğit senin o fakir babanın kamburunu dölüyle düzeltsin",
    "şahabettin ananın amına asansör kurup 10 kişiyle çıksın",
    "qq senin o köylü sülaleni şehrin ortasında sike sike inletsin",
    "ananın amına vapur yanaştırıp liman yapayım orospu dölü",
    "babanın tabutunu sikeyim ucube evladı mezarını sikeyim",
    "ananın amına kanca atıp denizde sikeyim balıklara yedireyim",
    "bacını pavyonda şampanya niyetine patlatayım",
    "kxrem senin o ucube sülaleni her gece kabusa çevirsin",
    "hasret ananın amına nükleer bomba atıp patlatsın",
    "yiğit bacını otogarda tır şoförlerine sermaye etsin",
    "şahabettin ananın o kara amcığını sike sike beyazlatsın",
    "qq senin o ucube hayatını sikeyim siktir git öl",
    "ananın amına mikserle girip ayran yapayım babana içireyim",
    "kxrem senin o ucube genlerini sike sike düzeltsin",
    "hasret bacının amcığını testereyle biçip silsilece siktirsin",
    "yiğit ananı her gece başka bir pavyonun önüne bağlasın",
    "şahabettin sülalendeki tüm kadınları köle pazarına satsın",
    "qq senin o süzme babanın mezarını dölle sulasın",
    "ananın amına kalorifer peteği sokup kışın ısınayım",
    "kxrem bacını sike sike dilsiz bırakıp kölesi yapsın",
    "hasret ananın amına tır makası sokup her gece inletsin",
    "yiğit senin o ucube varlığını yerle bir edip silsileni silsin",
    "şahabettin ananın amına dinamit döşeyip havaya uçursun",
    "qq senin o fakir ve zavallı onurunu sikeyim",
    "ananın amına beton mikseriyle girip anıt mezar yapayım",
    "kxrem sülalendeki her kadını sike sike delirsin",
    "hasret babanın kel kafasında dölüyle perküsyon çalsın",
    "yiğit ananın amına tünel açıp içinden metro geçirsin",
    "şahabettin bacının o dar amcığını sike sike mühürlesin",
    "qq senin doğduğun hastanenin başhekimini sikeyim",
    "ananın amına jeneratör sokup mahalleye elektrik vereyim",
    "kxrem ananın amına tazyikli su sıkıp temizledikten sonra siktirsin",
    "hasret senin o süzme sülaleni mezarlıkta sıraya dizsin",
    "yiğit ananın amına beton döküp dondurduktan sonra silsilece siktirsin",
    "şahabettin babanın mezar taşını sike sike toz etsin",
    "qq senin o ucube hayatını sikeyim siktir git geber",
    "ananın amına yangın söndürme tüpü boşaltıp kış uykusuna yatayım",
    "kxrem sülalendeki tüm bakireleri sıraya dizip siktirsin",
    "hasret ananın o buruşmuş amcığını jiletle kesip tuz bassın",
    "yiğit senin o ucube babanın kamburunu dölüyle düzeltsin",
    "şahabettin ananın amına asansör kurup her katta ayrı siktirsin",
    "qq senin o fakir sülaleni sike sike zengin edeyim"
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
        await context.bot.send_message(chat_id=OWNER_ID, text="🛑 OPERASYON DURDURULDU.")

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
