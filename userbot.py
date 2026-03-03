import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- 1. RENDER PORT AÇMA (EN BAŞTA OLMALI) ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_server():
    # Render'ın beklediği portu anında açıyoruz
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    print(f"Port {port} dinleniyor...")
    server.serve_forever()

# Portu bot başlamadan önce başka bir kolda (thread) hemen açıyoruz
Thread(target=run_server, daemon=True).start()

# --- 2. BOT AYARLARI ---
api_id = 30150271
api_hash = "bbe0e183c97ead8a86926ecb95938486"
session_string = "1BJWap1wBuxby9hSYUeqYoO_um3b2teWTX71R8lqGGpW8DBAQGG7rlbYCHrFzthXLCe2jZT36TDvZOEx08eZQzjTPS_pZ0xDX4wEYotrEkkGaUJwNE_6iZ8UZuBDBJX6PIb1xclOarZZoPZVWrP6qIzF1qwuq73m6cQhlf41pt5PUrkYcgat-Kc2xZYSUDTj96r5qhVXr8Fx6gfcq38eh9zt-CNc4sL9dLy_j5NCpjyCsNTBi0kF5mFI23Dws7hTGl8OvBhj-h7Ay8D4altC6f7CgjpmfYaQ0Ymp9K4EhSUGtsIqocex3S-Tbs1PrY16lC4xeY6Lg63rZ7bD4ciFa9W6Z8mvQxHQ="

client = TelegramClient(StringSession(session_string), api_id, api_hash)
AUTHORIZED_USERS = [6534222591, 8256872080, 8343507331]
lock_mode = {}

# --- 3. KOMUTLAR VE EVENTLER ---
@client.on(events.NewMessage(pattern=r'^/lock (.+)'))
async def lock_handler(event):
    if event.sender_id not in AUTHORIZED_USERS or not event.is_group: return
    mode = event.pattern_match.group(1).lower()
    lock_mode[event.chat_id] = mode
    await event.reply(f"🔒 Mod {mode} aktif.")

@client.on(events.MessageEdited)
async def edited_handler(event):
    if not event.is_group or not event.message.text: return
    try:
        await event.delete()
        sender = await event.get_sender()
        mention = f"[{sender.first_name}](tg://user?id={event.sender_id})"
        await event.respond(f"⚠️ {mention}, mesaj düzenlemek yasak!")
    except: pass

@client.on(events.NewMessage)
async def delete_handler(event):
    if not event.is_group or event.chat_id not in lock_mode: return
    mode = lock_mode[event.chat_id]
    if mode == "off" or mode == "0": return
    msg = event.message
    if mode == "1":
        try: await msg.delete()
        except: pass
    elif mode == "2":
        if msg.media and not msg.voice:
            try: await msg.delete()
            except: pass

# --- 4. ANA DÖNGÜ ---
async def main():
    print("Bot başlatılıyor...")
    await client.start()
    print("Bot Giriş Yaptı!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Python 3.14 uyumlu başlatma
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
