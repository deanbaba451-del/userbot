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
    return "Bot Aktif"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- AYARLAR ---
TOKEN = "8685088803:AAGomXnBLdQ-ZRz8Mzssl9dS7d_FlKU6zFY"
OWNER_ID = 6534222591
HEDEFLER = [] # ID listesi
SALDIRI_DURUMU = False
SPAM_HIZI = 0.8 # Hız ayarı

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
    "bacının amına bayrak direği sokup dalgalayım", "senin o ucube gen haritanı sikeyim",
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

async def ekle_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if not context.args:
        await update.message.reply_text("Lütfen bir @mention veya ID girin.")
        return
    
    target = context.args[0]
    HEDEFLER.append(target)
    await update.message.reply_text(f"Hedef eklendi: {target}")

async def bulk_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if not context.args:
        await update.message.reply_text("Lütfen @mentionları aralarında boşluk bırakarak yazın.")
        return
    
    for target in context.args:
        HEDEFLER.append(target)
    await update.message.reply_text(f"{len(context.args)} adet hedef listeye eklendi.")

async def baslat_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SALDIRI_DURUMU
    if update.effective_user.id != OWNER_ID: return
    
    if not HEDEFLER:
        await update.message.reply_text("Önce hedef ekle!")
        return

    SALDIRI_DURUMU = True
    await update.message.reply_text("Saldırı başlatıldı!")
    
    while SALDIRI_DURUMU:
        for hedef in HEDEFLER:
            if not SALDIRI_DURUMU: break
            try:
                soz = random.choice(sozler)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{hedef} {soz}")
                await asyncio.sleep(SPAM_HIZI)
            except Exception as e:
                print(f"Hata: {e}")
                await asyncio.sleep(1)

async def dur_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SALDIRI_DURUMU
    if update.effective_user.id == OWNER_ID:
        SALDIRI_DURUMU = False
        HEDEFLER.clear()
        await update.message.reply_text("Saldırı durduruldu ve liste temizlendi.")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler("ekle", ekle_komutu))
    app_bot.add_handler(CommandHandler("bulk", bulk_komutu))
    app_bot.add_handler(CommandHandler("baslat", baslat_komutu))
    app_bot.add_handler(CommandHandler("dur", dur_komutu)) # Ekstra: Durdurmak için
    
    print("Bot çalışıyor...")
    app_bot.run_polling()
