import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- RENDER HEALTH CHECK ---
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

AUTHORIZED_USERS = [6534222591, 8256872080, 8343507331]
active_loops = {} # Grup ID : True/False

# --- YENİ KOMUT: /loop [metin] ---
@client.on(events.NewMessage(pattern=r'^/loop (.+)'))
async def loop_handler(event):
    if event.sender_id not in AUTHORIZED_USERS: return
    
    chat_id = event.chat_id
    text = event.pattern_match.group(1)
    
    if text.lower() == "stop":
        active_loops[chat_id] = False
        await event.reply("🛑 Loop durduruldu.")
        return

    active_loops[chat_id] = True
    await event.delete() # Komutu sil
    
    while active_loops.get(chat_id):
        try:
            msg = await client.send_message(chat_id, text)
            await asyncio.sleep(0.1) # 0.1 saniye bekle
            await msg.delete()
        except Exception:
            await asyncio.sleep(1) # Flood hatası alırsan biraz daha fazla bekle

# --- DİĞER KOMUTLAR ---
@client.on(events.NewMessage(pattern=r'^/spam (.+) (\d+)'))
async def spam_handler(event):
    if event.sender_id not in AUTHORIZED_USERS: return
    text, count = event.pattern_match.group(1), int(event.pattern_match.group(2))
    for _ in range(count):
        await event.respond(text)
        await asyncio.sleep(0.2)

@client.on(events.NewMessage(pattern=r'^/medya (\d+)'))
async def media_timer_handler(event):
    if event.sender_id not in AUTHORIZED_USERS: return
    global media_clean_interval
    media_clean_interval = int(event.pattern_match.group(1))
    await event.reply(f"✅ Süre {media_clean_interval} saniye yapıldı.")

# --- ANA DÖNGÜ VE BAŞLATMA ---
async def main():
    Thread(target=run_server, daemon=True).start()
    await client.start()
    print("Bot ve Loop sistemi aktif!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
