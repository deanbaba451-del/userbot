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
TOKEN = "BOT_TOKEN_BURAYA"
OWNER_ID = 6534222591
HEDEFLER = set()
AKTIF_MESAJLAR = {} # Her user_id için en son mesaj id'sini tutar

sozler = [
    "siktir git öl", "ananın amcığını sikiyim", "emekli babanın kel kafasına döllerimi dökeyim",
    "şahabettin anneni siksin", "orospunhn çocuğu seni", "yaz yaz", "o amele babanın kamburunu sikerim",
    "salak ucube orospu çocuğu", "o ananın amcığındaki yumurtaları yerim", "amına doğumun oğlu",
    "qq anneni siksin", "annen şahabbetine amcığını yedirdi", "ölmüşlerinin mezarına çiçek yerine dildo koyarım",
    "regl ananın kanını babana içiririm", "otobanda otostop çeken bacına 250km hızla çarparım",
    "o ananın amına koç taşşağı fırlatırım", "ananı 7 kule zindanlarına atar sike sike kölem ederim",
    "o ananın sırtına binip at gibi kişnete kişnete sikeyim", "annenin göt deliğini parmaklarım sonra boklu parmagımı kendi götüme sokarım",
    "o ananın amında saltanat kurar hüküm sürerim orospu çocuğu", "ananın ölüsünü sikeyim", "babanın mezarını sikeyim",
    "bacının amcığına beton dökeyim", "o ananın amına tır sokayım", "soyunun sopunun amına koyayım",
    "senin tipini sikeyim ucube", "ananın amına kireç dökerim", "babanın sakalını sikeyim", "bacını pazarda satayım",
    "o ananın amına kaktüs sokayım", "senin ben doğduğun günü sikeyim", "ananın amına tekmeyle gireyim",
    "babanın kemiklerini sikeyim", "orospu evladı seni", "ananın amını parçalarım", "seni sike sike öldürürüm",
    "babanın kafa tasını sikeyim", "ananın götüne kazık çakayım", "bacının amına dildo sokayım",
    "senin o ucube sıfatını sikeyim", "ananın amına uçak indiririm", "babanın bıyığını sikeyim",
    "senin sülaleni sikeyim", "ananın amına dinamit lokumu döşeyim", "bacının amını deşeyim",
    "senin ben karakterini sikeyim", "ananın amına hortum sokayım", "babanın mezarındaki toprakları sikeyim",
    "o ananın amını darmadağın ederim", "ananın amına soba borusu sokup ısınayım", "senin o sülalendeki bütün kadınları üst üste koyup sikeyim",
    "babanın tabutunu sikeyim orospu dölü", "ananın amına ranzayla girerim", "senin o ezik genlerini sikeyim",
    "bacının amına bayrak direği sokayım", "ananın göt deliğine asit dökeyim", "senin ben cibiliyetini sikeyim",
    "babanın mezarındaki çiçekleri sikeyim", "ananı her gece başka mahallede siktireyim", "senin o süzme orospu anneni sikeyim",
    "ananın amına çapa atayım", "bacının amcığını testereyle keseyim", "senin varlığını sikeyim ucube evladı",
    "babanın kamburundaki her kemiği sikeyim", "ananın amına vapur yanaştırayım", "seni doğurtan ebenin parmaklarını sikeyim",
    "ananın amında mangal yapayım", "senin sülalendeki ölüleri diriltip sikeyim", "ananın götüne şemsiye sokup açayım",
    "babanın ölüsünü sikeyim", "ananın amına beton mikseri sokayım", "senin o fakir fukara sülaleni sikeyim",
    "ananı sike sike komaya sokayım", "bacının amına matkapla gireyim", "senin o silik karakterini sikeyim",
    "ananın amına nükleer bomba atayım", "babanın mezar taşını sikeyim", "ananın amına yangın tüpü boşaltayım",
    "seni doğuran o ananın amcığını sikeyim", "ananın amına elektrik direği sokayım", "senin o köylü babanın kasketini sikeyim",
    "ananın amına jeneratör sokayım", "bacının götünü sike sike kanatayım", "senin sülaleni mezarlıkta sikeyim",
    "ananın amına tazyikli su sıkayım", "babanın o amele suratını sikeyim", "ananı pavyon köşelerinde sikeyim",
    "senin o ucube varlığını ortadan kaldırayım", "ananın amına asansör kurayım", "bacının amcığını sike sike çürüteyim",
    "senin o köhne sülaleni sikeyim", "ananın amına foseptik çukuru açayım", "babanın o kambur sırtını sikeyim",
    "ananı sike sike öldürüp mezara gömeyim", "senin o beyinsiz kafanı sikeyim", "ananın amına tır dorsesi sokayım",
    "bacını sike sike dilsiz bırakayım", "senin o ucube gen haritanı sikeyim", "ananın amına tünel açayım",
    "babanın o ölü gözlerini sikeyim", "ananı sike sike sokağa atayım", "senin o zavallı hayatını sikeyim",
    "ananın amına kepçe sokayım", "bacının o ucube amcığını sikeyim", "senin o fakir ruhunu sikeyim",
    "ananın amına kanca atayım", "babanın o çürümüş dişlerini sikeyim", "ananı sike sike delirteyim",
    "senin o ucube suratına dölümü boşaltayım", "ananın amına kalorifer kazanı sokayım", "bacının o amcığını sike sike patlatayım",
    "senin sülalendeki her kadını sikeyim", "ananın amına matkapla gireyim", "babanın o ucube mezarını sikeyim"
]

async def spam_dongusu(context, chat_id, user_id, msg_id):
    # Bu döngü sadece mesaj "güncel" ise devam eder
    while user_id in HEDEFLER and AKTIF_MESAJLAR.get(user_id) == msg_id:
        try:
            cevap = random.choice(sozler)
            await context.bot.send_message(chat_id=chat_id, text=cevap, reply_to_message_id=msg_id)
            await asyncio.sleep(2)
        except:
            break

async def target_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        HEDEFLER.clear()
        AKTIF_MESAJLAR.clear()
        try:
            target_id = None
            if update.message.reply_to_message:
                target_id = update.message.reply_to_message.from_user.id
            elif context.args:
                target_id = int(context.args[0].strip())
            
            if target_id:
                HEDEFLER.add(target_id)
                await update.message.reply_text(f"{target_id} hedef yapıldı")
        except: pass

async def bulk_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        HEDEFLER.clear()
        AKTIF_MESAJLAR.clear()
        raw_ids = " ".join(context.args).replace("@", "").split(",")
        for r_id in raw_ids:
            if r_id.strip().isdigit():
                HEDEFLER.add(int(r_id.strip()))
        await update.message.reply_text(f"{len(HEDEFLER)} kişi listeye eklendi")

async def tetikleyici(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    msg_id = update.message.message_id
    text = update.message.text

    if text.lower() == "/yigit" and user_id == OWNER_ID:
        HEDEFLER.clear()
        AKTIF_MESAJLAR.clear()
        await context.bot.send_message(chat_id=chat_id, text="tmm", reply_to_message_id=msg_id)
        return

    if user_id in HEDEFLER:
        # En son mesaj id'sini güncelle (bot artık bu mesaj üzerinden devam edecek)
        AKTIF_MESAJLAR[user_id] = msg_id
        # Paralel görev başlat (diğer hedefleri engellemez)
        asyncio.create_task(spam_dongusu(context, chat_id, user_id, msg_id))

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("target", target_ekle))
    app_bot.add_handler(CommandHandler("bulk", bulk_ekle))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), tetikleyici))
    app_bot.run_polling()
