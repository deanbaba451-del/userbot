import os
import asyncio
import threading
import random
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

app = Flask('')

@app.route('/')
def home():
    return "bot aktif"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- AYARLAR ---
TOKEN = "8685088803:AAGomXnBLdQ-ZRz8Mzssl9dS7d_FlKU6zFY"
OWNER_ID = 6534222591
HEDEFLER = {} 
AKTIF_MESAJLAR = {} 
SALDIRI_DURUMU = False
SPAM_HIZI = 2 

sozler = [
    "siktir git çık gruptan ananı sikeyim", "o ucube tipinle bu grupta ne işin var anasını siktiğim",
    "çık gruptan yoksa ananın amcığına beton dökerim", "gruptan çık ucube dölü ananı sike sike öldürürüm",
    "senin bu grupta nefes alışını sikeyim ucube evladı", "ananın amına ranzayla girerim gruptan siktir git",
    "o amele babanın kamburunu sikeyim çık şu gruptan", "senin o ucube varlığını gruptan kazırım",
    "gruptan çıkmazsan ananın amına nükleer bomba atarım", "siktir git öl ucube evladı", 
    "ananın o süzme amcığını sikiyim", "emekli babanın kel kafasına döllerimi dökeyim",
    "orospunun öz evladı seni", "ananın amcığındaki yumurtaları tek tek yutayım",
    "amına doğumun ucube dölü", "qq annenle grup yapsın orospu evladı", 
    "ölmüşlerinin mezarına çiçek yerine dildo dikeyim", "regl ananın kanını babana şarap niyetine içireyim", 
    "otobanda otostop çeken bacına tırla çarpıp sikeyim", "o ananın amına koç taşşağı fırlatayım", 
    "ananı 7 kule zindanlarına atar sike sike kölem edeyim", "o ananın sırtına binip kırbaçla sikeyim", 
    "ananın amında saltanat kurar hüküm sürerim", "babanın mezarındaki toprakları sike sike çamur edeyim", 
    "bacının amcığına beton döküp heykelini sikeyim", "ananın amına tır dorsesi sokup park edeyim", 
    "senin doğduğun hastaneyi sülaleni sikeyim", "babanın tabutunu sikeyim orospu artığı", 
    "bacının amına bayrak direği sokup dalgalandırayım", "senin o ucube gen haritanı sikeyim",
    "ananın amına jeneratör sokup elektrik üreteyim", "babanın o çürümüş dişlerini sike sike dökeyim",
    "ananın amına kalorifer kazanı sokup ısıtayım", "bacının o ucube amcığını sike sike çürüteyim",
    "senin o fakir ruhunu sülaleni sikeyim", "ananın amına kanca atıp denizde sikeyim",
    "babanın kambur sırtında dölümle resim yapayım", "ananı sike sike öldürüp mezarını sikeyim",
    "senin o beyinsiz kafatasını sikeyim", "bacını sike sike dilsiz bırakıp kölem yapayım",
    "ananın amına asansör kurup inip çıkayım", "senin o ucube varlığını galaksiden sileyim",
    "ananın amına foseptik çukuru açıp içine sikeyim", "babanın mezar taşını sikeyim ucube dölü",
    "ananın amına yangın tüpü boşaltıp söndüreyim", "seni doğuran o ananın amcığını sikeyim",
    "ananın amına elektrik direği sokup trafo yapayım", "senin o köylü babanın kasketini sikeyim",
    "ananın amına jeneratör sokup mahallece sikelim", "bacının götünü sike sike kanatıp içeyim",
    "senin sülaleni mezarlıkta sıraya dizip sikeyim", "ananın amına tazyikli su sıkıp temizleyeyim",
    "babanın o amele suratına boşalayım", "ananı pavyon köşelerinde siktire siktire öldüreyim",
    "senin o ucube varlığını yerle bir edeyim", "ananın amına asansör kurup kat kat sikeyim",
    "bacının amcığını sike sike patlatayım", "senin o köhne sülaleni sikeyim",
    "ananın amına kepçe sokup kanalizasyon yapayım", "babanın o kambur belini sikeyim",
    "senin o ucube suratına dölümü fışkırtayım", "ananın amına tünel açıp içinden geçeyim",
    "babanın o ölü gözlerini sikeyim", "ananı sike sike sokağa atıp rezil edeyim",
    "senin o zavallı hayatını sülaleni sikeyim", "ananın amına matkapla girip delik deşik edeyim",
    "bacının o ucube amcığını sikeyim", "senin o fakir sülaleni sikeyim",
    "ananın amına kireç döküp yakayım", "babanın mezarındaki çiçekleri sikeyim",
    "ananı her gece başka mahallede siktireyim", "senin o süzme orospu anneni sikeyim",
    "ananın amına çapa atayım", "bacının amcığını testereyle kesip sikeyim",
    "senin varlığını sikeyim ucube evladı", "babanın kamburundaki her kemiği tek tek sikeyim",
    "ananın amına vapur yanaştırıp liman yapayım", "seni doğuran ebenin parmaklarını sikeyim",
    "ananın amında mangal yapıp babana yedireyim", "senin sülalendeki ölüleri diriltip sikeyim",
    "ananın götüne şemsiye sokup içinde açayım", "babanın o ölü suratını sikeyim",
    "ananın amına beton mikseri sokup dondurayım", "ananın amına tır makası sokup sikeyim",
    "bacını kurban pazarında siktireyim", "senin o ucube soyunu sopunu kurutayım",
    "ananın amına dinamit döşeyip patlatayım", "babanın o çürük mezarını sike sike deşeyim",
    "ananı sike sike gökyüzüne fırlatayım", "senin o süzme ucube canını sikeyim",
    "ananın amına kalorifer peteği sokup ısıtayım", "bacının o ucube amını sike sike patlatayım",
    "ananın o amcığını sike sike mühürleyeyim", "senin o ucube babanın mezarındaki toprakları sikeyim",
    "ananın amına nükleer santral kurayım", "senin sülalendeki her kadını sike sike delirteyim"
]

async def start_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        mesaj = (
            "selam hasret,\n\n"
            "komutlar:\n"
            "/target - id yaz veya yanıtla (hedef seçer)\n"
            "/bulk - id1,id2 (çoklu hedef seçer)\n"
            "/hasret [hız] - saldırıyı başlatır (örn: /hasret 1.5)\n"
            "/yigit - saldırıyı durdurur ve listeyi siler\n\n"
            "raporlar artık dm'den gelecek."
        )
        await update.message.reply_text(mesaj)

async def spam_dongusu(context, chat_id, user_id, msg_id):
    isim = HEDEFLER.get(user_id, "")
    prefix = f"{isim.lower()} " if isim else ""
    
    while SALDIRI_DURUMU and user_id in HEDEFLER and AKTIF_MESAJLAR.get(user_id) == msg_id:
        try:
            cevap = random.choice(sozler)
            await context.bot.send_message(chat_id=chat_id, text=f"{prefix}{cevap}", reply_to_message_id=msg_id)
            await asyncio.sleep(SPAM_HIZI)
        except:
            break

async def target_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        try:
            target_user = None
            if update.message.reply_to_message:
                target_user = update.message.reply_to_message.from_user
            elif context.args:
                uid = int(context.args[0].strip())
                target_user = (await context.bot.get_chat_member(update.effective_chat.id, uid)).user
            
            if target_user:
                name = target_user.first_name if target_user.first_name else ""
                HEDEFLER[target_user.id] = name
                await update.message.reply_text(f"hedef: {name} ({target_user.id})")
        except: pass

async def bulk_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        raw_ids = " ".join(context.args).replace("@", "").split(",")
        for r_id in raw_ids:
            if r_id.strip().isdigit():
                uid = int(r_id.strip())
                HEDEFLER[uid] = ""
        await update.message.reply_text(f"{len(HEDEFLER)} kişi hedefe eklendi")

async def genel_isleyici(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SALDIRI_DURUMU, SPAM_HIZI
    if not update.message or not update.message.text: return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    msg_id = update.message.id
    text = update.message.text.lower()

    if user_id == OWNER_ID:
        if text.startswith("/hasret"):
            SALDIRI_DURUMU = True
            try:
                args = text.split()
                if len(args) > 1: SPAM_HIZI = float(args[1])
            except: SPAM_HIZI = 2
            await update.message.reply_text(f"başladı (hız: {SPAM_HIZI}s)")
            return
        
        if text == "/yigit":
            SALDIRI_DURUMU = False
            HEDEFLER.clear()
            AKTIF_MESAJLAR.clear()
            await update.message.reply_text("tmm")
            return

    if SALDIRI_DURUMU and user_id in HEDEFLER:
        try:
            await context.bot.send_message(chat_id=OWNER_ID, text="sikme hazır")
        except: pass
        AKTIF_MESAJLAR[user_id] = msg_id
        asyncio.create_task(spam_dongusu(context, chat_id, user_id, msg_id))

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start_komutu))
    app_bot.add_handler(CommandHandler("target", target_ekle))
    app_bot.add_handler(CommandHandler("bulk", bulk_ekle))
    app_bot.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), genel_isleyici))
    
    app_bot.run_polling()
