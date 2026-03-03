from telethon import TelegramClient, events
import os
import re

api_id = int(os.getenv("30150271"))
api_hash = os.getenv("bbe0e183c97ead8a86926ecb95938486")

client = TelegramClient("mysession", api_id, api_hash)

# Komut kullanabilecek ID'ler
AUTHORIZED_USERS = [6534222591, 8256872080]

lock_mode = {}  # grup_id : mod

# LOCK KOMUTU
@client.on(events.NewMessage(pattern=r'^/lock (.+)'))
async def lock_handler(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return

    if not event.is_group:
        return

    mode = event.pattern_match.group(1).lower()
    chat_id = event.chat_id

    if mode == "1":
        lock_mode[chat_id] = 1
        await event.reply("🔒 Lock 1 aktif (Medya + link silinir)")
    elif mode == "2":
        lock_mode[chat_id] = 2
        await event.reply("🔒 Lock 2 aktif (Sadece metin + ses serbest)")
    elif mode == "off":
        lock_mode[chat_id] = 0
        await event.reply("🔓 Lock kapatıldı")
    else:
        await event.reply("Kullanım: /lock 1 | /lock 2 | /lock off")

# MESAJ KONTROL
@client.on(events.NewMessage)
async def delete_handler(event):
    if not event.is_group:
        return

    chat_id = event.chat_id

    if chat_id not in lock_mode:
        return

    mode = lock_mode[chat_id]

    if mode == 0:
        return

    message = event.message

    # 🔒 LOCK 1 → Medya + link sil
    if mode == 1:
        if message.media:
            await message.delete()
            return

        if message.text and re.search(r'https?://|t\.me', message.text):
            await message.delete()
            return

    # 🔒 LOCK 2 → Sadece metin + ses kalsın
    if mode == 2:
        # Sesli mesaj serbest
        if message.voice:
            return

        # Metin serbest (link olsa bile kalır)
        if message.text:
            return

        # Diğer her şey silinir
        await message.delete()

client.start()
client.run_until_disconnected()