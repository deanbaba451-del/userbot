import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER'IN BOTU KAPATMASINI ENGELLEYEN BÖLÜM ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_server():
    # Render otomatik bir PORT atar, o portu dinlemezsek botu kapatır.
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# --- BOT BİLGİLERİ VE GİRİŞ ---
api_id = 30150271
api_hash = "bbe0e183c97ead8a86926ecb95938486"
session_string = "1BJWap1wBuxby9hSYUeqYoO_um3b2teWTX71R8lqGGpW8DBAQGG7rlbYCHrFzthXLCe2jZT36TDvZOEx08eZQzjTPS_pZ0xDX4wEYotrEkkGaUJwNE_6iZ8UZuBDBJX6PIb1xclOarZZoPZVWrP6qIzF1qwuq73m6cQhlf41pt5PUrkYcgat-Kc2xZYSUDTj96r5qhVXr8Fx6gfcq38eh9zt-CNc4sL9dLy_j5NCpjyCsNTBi0kF5mFI23Dws7hTGl8OvBhj-h7Ay8D4altC6f7CgjpmfYaQ0Ymp9K4EhSUGtsIqocex3S-Tbs1PrY16lC4xeY6Lg63rZ7bD4ciFa9W6Z8mvQxHQ="

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Yetkili Kullanıcılar
AUTHORIZED_USERS = [6534222591, 8256872080]
lock_mode = {}

# --- KOMUTLAR ---
@client.on(events.NewMessage(pattern=r'^/lock (.+)'))
async def lock_handler(event):
    if event.sender_id not in AUTHORIZED_USERS or not event.is_group:
        return

    mode = event.pattern_match.group(1).lower()
    chat_id = event.chat_id

    if mode == "1":
        lock_mode[chat_id] = 1
        await event.reply("🔒 **Lock 1 aktif** (Medya ve Linkler yasak)")
    elif mode == "2":
        lock_mode[chat_id] = 2
        await event.reply("🔒 **Lock 2 aktif** (Sadece Metin ve Ses serbest)")
    elif mode == "off":
        lock_mode[chat_id] = 0
        await event.reply("🔓 **Kilitler açıldı**")

# --- MESAJ KONTROLÜ ---
@client.on(events.NewMessage)
async def delete_handler(event):
    if not event.is_group or event.chat_id not in lock_mode:
        return

    mode = lock_mode[event.chat_id]
    if mode == 0: return

    msg = event.message

    if mode == 1:
        # Medya varsa veya mesajda link/t.me adresi geçiyorsa sil
        if msg.media or (msg.text and re.search(r'https?://|t\.me', msg.text)):
            try: await msg.delete()
            except: pass

    elif mode == 2:
        # Sesli mesaj (voice) serbest, diğer medyalar yasak
        if msg.media and not msg.voice:
            try: await msg.delete()
            except: pass

# --- ÇALIŞTIRMA ---
if __name__ == '__main__':
    # Web sunucusunu arka planda başlat
    Thread(target=run_server, daemon=True).start()
    
    print("Bot Render üzerinde sorunsuz başlatılıyor...")
    client.start()
    client.run_until_disconnected()
