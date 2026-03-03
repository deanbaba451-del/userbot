import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER HEALTH CHECK (7/24 KALMASI İÇİN) ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# --- BOT AYARLARI ---
api_id = 30150271
api_hash = "bbe0e183c97ead8a86926ecb95938486"
session_string = "1BJWap1wBuxby9hSYUeqYoO_um3b2teWTX71R8lqGGpW8DBAQGG7rlbYCHrFzthXLCe2jZT36TDvZOEx08eZQzjTPS_pZ0xDX4wEYotrEkkGaUJwNE_6iZ8UZuBDBJX6PIb1xclOarZZoPZVWrP6qIzF1qwuq73m6cQhlf41pt5PUrkYcgat-Kc2xZYSUDTj96r5qhVXr8Fx6gfcq38eh9zt-CNc4sL9dLy_j5NCpjyCsNTBi0kF5mFI23Dws7hTGl8OvBhj-h7Ay8D4altC6f7CgjpmfYaQ0Ymp9K4EhSUGtsIqocex3S-Tbs1PrY16lC4xeY6Lg63rZ7bD4ciFa9W6Z8mvQxHQ="

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Yetkili ID'ler
AUTHORIZED_USERS = [6534222591, 8256872080, 8343507331]
lock_mode = {}
media_clean_target = -1003626403225 # Hedef Grup ID
media_clean_interval = 180 # Varsayılan 3 dakika

# --- KOMUTLAR ---

# /medya [saniye] -> Otomatik silme süresini ayarlar
@client.on(events.NewMessage(pattern=r'^/medya (\d+)'))
async def media_timer_handler(event):
    if event.sender_id not in AUTHORIZED_USERS: return
    global media_clean_interval
    media_clean_interval = int(event.pattern_match.group(1))
    await event.reply(f"✅ Medya temizleme döngüsü {media_clean_interval} saniye olarak ayarlandı.")

# /lock [1/2/off] -> Grup kilit modları
@client.on(events.NewMessage(pattern=r'^/lock (.+)'))
async def lock_handler(event):
    if event.sender_id not in AUTHORIZED_USERS or not event.is_group: return
    mode = event.pattern_match.group(1).lower()
    chat_id = event.chat_id

    if mode == "1":
        lock_mode[chat_id] = 1
        await event.reply("🔒 **Lock 1 aktif** (Medya ve Link yasak)")
    elif mode == "2":
        lock_mode[chat_id] = 2
        await event.reply("🔒 **Lock 2 aktif** (Sadece Metin ve Ses serbest)")
    elif mode == "off":
        lock_mode[chat_id] = 0
        await event.reply("🔓 **Kilitler kapatıldı.**")

# --- OTOMATİK SİSTEMLER ---

# Belirli gruptaki medyaları süreli temizleyen döngü
async def auto_media_cleaner():
    while True:
        try:
            async for message in client.iter_messages(media_clean_target, limit=100):
                if message.media:
                    await message.delete()
        except Exception as e:
            print(f"Temizleme hatası: {e}")
        await asyncio.sleep(media_clean_interval)

# Gruptaki anlık mesaj kontrolü (Lock modları için)
@client.on(events.NewMessage)
async def delete_handler(event):
    if not event.is_group or event.chat_id not in lock_mode: return
    mode = lock_mode[event.chat_id]
    if mode == 0: return

    msg = event.message
    if mode == 1:
        if msg.media or (msg.text and re.search(r'https?://|t\.me', msg.text)):
            try: await msg.delete()
            except: pass
    elif mode == 2:
        if msg.media and not msg.voice:
            try: await msg.delete()
            except: pass

# --- ANA BAŞLATICI ---
async def main():
    print("Bot başlatılıyor...")
    Thread(target=run_server, daemon=True).start()
    await client.start()
    
    # Arka plan temizlik görevini başlat
    asyncio.create_task(auto_media_cleaner())
    
    print("Bot Render üzerinde sorunsuz çalışıyor!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
