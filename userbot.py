import os
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
        await event.reply("🔒 **Lock 1 aktif** (Her şey siliniyor)")
    elif mode == "2":
        lock_mode[chat_id] = 2
        await event.reply("🔒 **Lock 2 aktif** (Metin ve Ses serbest, diğerleri yasak)")
    elif mode == "off":
        lock_mode[chat_id] = 0
        await event.reply("🔓 **Kilit kapatıldı.**")

# --- MESAJ DÜZENLEME KONTROLÜ (TEPKİ HATASI DÜZELTİLDİ) ---
@client.on(events.MessageEdited)
async def edited_handler(event):
    if not event.is_group:
        return
    
    # Eğer düzenlenen şey mesajın içeriği (text) değilse (yani tepki ise), görmezden gel
    if not event.message.text:
        return

    try:
        # Düzenlenen mesajı sil
        await event.delete()
        # Düzenleyen kişiyi etiketle ve uyar
        sender = await event.get_sender()
        name = sender.first_name if sender.first_name else "Kullanıcı"
        mention = f"[{name}](tg://user?id={event.sender_id})"
        await event.respond(f"⚠️ {mention}, mesaj düzenlemek yasak!")
    except:
        pass

# --- SİLME MANTIĞI ---
@client.on(events.NewMessage)
async def delete_handler(event):
    if not event.is_group or event.chat_id not in lock_mode:
        return
    
    mode = lock_mode[event.chat_id]
    if mode == 0:
        return

    msg = event.message

    if mode == 1:
        try: await msg.delete()
        except: pass

    elif mode == 2:
        # Mesajda medya varsa ve bu bir ses kaydı (voice) değilse sil
        if msg.media and not msg.voice:
            try: await msg.delete()
            except: pass

# --- BAŞLATICI ---
async def main():
    print("Bot başlatılıyor...")
    Thread(target=run_server, daemon=True).start()
    await client.start()
    print("Bot Render üzerinde sorunsuz çalışıyor!")
