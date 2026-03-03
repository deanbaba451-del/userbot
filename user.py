import os
import re
from telethon import TelegramClient, events
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER PORT HATASINI ENGELLEMEK İÇİN (HEALTH CHECK) ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# --- BOT AYARLARI ---
api_id = 30150271
api_hash = "bbe0e183c97ead8a86926ecb95938486"

# 'mysession' ismi, yüklediğin mysession.session dosyasıyla aynı olmalı
client = TelegramClient("mysession", api_id, api_hash)

AUTHORIZED_USERS = [6534222591, 8256872080]
lock_mode = {}

@client.on(events.NewMessage(pattern=r'^/lock (.+)'))
async def lock_handler(event):
    if event.sender_id not in AUTHORIZED_USERS or not event.is_group:
        return

    mode = event.pattern_match.group(1).lower()
    chat_id = event.chat_id

    if mode == "1":
        lock_mode[chat_id] = 1
        await event.reply("🔒 Lock 1 aktif (Medya + link silinir)")
    elif mode == "2":
        lock_mode[chat_id] = 2
        await event.reply("🔒 Lock 2 aktif (Metin + ses serbest)")
    elif mode == "off":
        lock_mode[chat_id] = 0
        await event.reply("🔓 Lock kapatıldı")

@client.on(events.NewMessage)
async def delete_handler(event):
    if not event.is_group or event.chat_id not in lock_mode:
        return

    mode = lock_mode[event.chat_id]
    if mode == 0: return

    msg = event.message

    if mode == 1:
        if msg.media or (msg.text and re.search(r'https?://|t\.me', msg.text)):
            try: await msg.delete()
            except: pass

    elif mode == 2:
        # Sadece ses (voice) ve saf metin (media olmayan) kalsın
        if not msg.voice and msg.media:
            try: await msg.delete()
            except: pass

# --- BAŞLAT ---
if __name__ == '__main__':
    # Render'ın botu kapatmaması için web server'ı başlatıyoruz
    Thread(target=run_server, daemon=True).start()
    
    print("Bot Render üzerinde başlatılıyor...")
    client.start()
    client.run_until_disconnected()
