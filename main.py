import os
import asyncio
import json
from threading import Thread
from flask import Flask
from pyrogram import Client, filters, enums, idle
from pyrogram.errors import UserNotParticipant, UserAlreadyParticipant

# --- CONFIGURATION ---
API_ID = 37314366
API_HASH = "bd4c934697e7e91942ac911a5a287b46"

# ✅ SESSION STRING
SESSION_STRING = "AQI5Xz4AxQryFBEInZokcDHtOY-r3t62LsBtM8rBOMNWUfHMQtG1CpbugFzxwpoW17c0uiaESKbdVjzuFypvE4mwomY4IaXCJ3KQ2OBpJNHbDMp6yNFFzTBDsbsGfpqL-lYB4iKZKfHksMbYlZxDMru02Wx4J4bahj4gWcZZfhg0FeE1p2hNnbMUf0QMzivSpGaPFfbOLDToRTELqaYH_16VjbTUlUbj3_7HFvJgb48zoHA8ENXCn4Hlv4RK4W6NPO2JrcQYlJe1aWJ4bqI182zGv7JS1FykApHe8Tm1kY36zVIwZtp2nfQyUrvkM3OIyfuIX3dhDfTrFXHZ2hGHYvl7Tl48agAAAAHyhnG8AA"

# 🎯 DATA SOURCE
TARGET_USERNAME = "Anysnapworld"  

# 👑 BRANDING
NEW_FOOTER = "⚡ Designed & Powered by @XLDAREDEVIL"

# --- 🔐 SECURITY SETTINGS ---
ALLOWED_GROUPS = [-1003387459132]

# ✅ CHANNELS
FSUB_CONFIG = [
    {"username": "Daredevilxlhub", "link": "https://t.me/Daredevilxlhub"},
    {"username": "daredevil_tm_group", "link": "https://t.me/daredevil_tm_group"}
]

# --- 🌐 FLASK KEEP ALIVE (FOR RENDER) ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🔥 Dark Devil Bot is Running on Render!"

def run_web():
    # Render assigns a port automatically via os.environ
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- PYROGRAM CLIENT ---
app = Client("dark_devil_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- HELPER: CHECK IF USER JOINED ---
async def check_user_joined(client, user_id):
    missing = False
    for ch in FSUB_CONFIG:
        try:
            member = await client.get_chat_member(ch["username"], user_id)
            if member.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                missing = True
                break
        except UserNotParticipant:
            missing = True
            break
        except Exception:
            pass
    return not missing 

# --- DASHBOARD ---
@app.on_message(filters.command(["start", "help", "menu"], prefixes="/") & (filters.private | filters.chat(ALLOWED_GROUPS)))
async def show_dashboard(client, message):
    if not await check_user_joined(client, message.from_user.id):
        return await message.reply_text(
            "🚫 **Access Denied!**\n\n"
            "Bot use karne ke liye pehle niche diye gaye channels join karein:\n\n"
            "📢 **[Click to Join Channel](https://t.me/Daredevilxlhub)**\n"
            "👥 **[Click to Join Group](https://t.me/daredevil_tm_group)**\n\n"
            "__Join karne ke baad dubara /start dabayein.__",
            disable_web_page_preview=True
        )

    text = (
        "📖 **DARK DEVIL DASHBOARD**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📢 **Channel:** [Join Here](https://t.me/Daredevilxlhub)\n"
        "👥 **Group:** [Join Here](https://t.me/daredevil_tm_group)\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "ᴍᴏʙɪʟᴇ: `/num 98XXXXXX10`\n"
        "ᴀᴀᴅʜᴀᴀʀ: `/aadhaar 1234XXXX9012`\n"
        "ɢsᴛ: `/gst 24ABCDE1234F1Z5`\n"
        "ɪғsᴄ: `/ifsc SBIN0000000`\n"
        "ᴜᴘɪ: `/upi username@bank`\n"
        "ғᴀᴍ: `/fam username@fam`\n"
        "ᴠᴇʜɪᴄʟᴇ: `/vehicle GJ01AB1234`\n"
        "ᴛᴇʟᴇɢʀᴀᴍ: `/tg @username`\n"
        "ᴛʀᴀᴄᴇ: `/trace 98XXXXXXXX`\n"
        "ɢᴍᴀɪʟ: `/gmail example@gmail.com`\n\n"
        "⚠️ **Note:** Result 30 seconds mein auto-delete ho jayega.\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{NEW_FOOTER}"
    )
    await message.reply_text(text, disable_web_page_preview=True)

# --- MAIN LOGIC ---
@app.on_message(filters.command(["num", "aadhaar", "gst", "ifsc", "upi", "fam", "vehicle", "tg", "trace", "gmail"], prefixes="/") & (filters.private | filters.chat(ALLOWED_GROUPS)))
async def process_request(client, message):
    
    if not await check_user_joined(client, message.from_user.id):
        return await message.reply_text(
            "🚫 **Access Denied!**\n\n"
            "Result dekhne ke liye pehle join karein:\n\n"
            "➡️ **[Join Channel](https://t.me/Daredevilxlhub)**\n"
            "➡️ **[Join Group](https://t.me/daredevil_tm_group)**\n\n"
            f"__Join karne ke baad wapas `/{message.command[0]}` bhejein.__",
            disable_web_page_preview=True
        )

    if len(message.command) < 2:
        return await message.reply_text(f"❌ **Data Missing!**\nUsage: `/{message.command[0]} <value>`")

    status_msg = await message.reply_text(f"🔍 **Searching via Dark Devil...**")

    try:
        sent_req = await client.send_message(TARGET_USERNAME, message.text)
        target_response = None

        for attempt in range(20):
            await asyncio.sleep(2.5)
            async for log in client.get_chat_history(TARGET_USERNAME, limit=5):
                if log.reply_to_message_id == sent_req.id:
                    text_content = (log.text or log.caption or "").lower()
                    ignore_words = ["wait", "processing", "searching", "scanning", "generating", "loading", "checking"]
                    if any(word in text_content for word in ignore_words):
                        await status_msg.edit(f"⏳ **Dark Devil Processing... (Attempt {attempt+1})**")
                        break 
                    target_response = log
                    break 
            if target_response: break

        if not target_response:
            await status_msg.edit(f"❌ **Timeout:** Server se reply nahi aaya.")
            return

        raw_text = ""
        if target_response.document:
            await status_msg.edit("📂 **Downloading & Parsing File...**")
            file_path = await client.download_media(target_response)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
            os.remove(file_path)
        elif target_response.photo:
            raw_text = target_response.caption or ""
        elif target_response.text:
            raw_text = target_response.text

        if not raw_text or len(raw_text.strip()) < 5:
            await status_msg.edit("❌ **No Data Found**")
            return

        json_data = {
            "status": "success",
            "service": "Dark Devil Lookup",
            "source": f"@{TARGET_USERNAME}",
            "query_type": message.command[0],
            "input": message.command[1],
            "raw_result": raw_text.strip(),
            "credits": NEW_FOOTER
        }

        final_json_str = json.dumps(json_data, indent=4, ensure_ascii=False)
        formatted_output = f"```json\n{final_json_str}\n```"

        sent_results = []
        if len(formatted_output) > 4000:
            msg1 = await message.reply_text(formatted_output[:4000])
            msg2 = await message.reply_text(formatted_output[4000:])
            sent_results.extend([msg1, msg2])
        else:
            msg = await message.reply_text(formatted_output)
            sent_results.append(msg)

        await status_msg.delete()
        await asyncio.sleep(30)
        for msg in sent_results:
            try: await msg.delete()
            except: pass

    except Exception as e:
        await status_msg.edit(f"❌ **Error:** {str(e)}")

# --- STARTUP LOGIC ---
async def start_bot():
    print("🚀 Starting Dark Devil Bot...")
    await app.start()
    
    print(f"🔄 Connecting to Data Source: @{TARGET_USERNAME}...")
    try:
        chat = await app.get_chat(TARGET_USERNAME)
        print(f"✅ Connected to: {chat.title} (ID: {chat.id})")
        if chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL, enums.ChatType.GROUP]:
            try:
                await app.join_chat(TARGET_USERNAME)
                print("✅ Joined Data Source Successfully!")
            except UserAlreadyParticipant:
                print("✅ Already Connected.")
            except Exception:
                pass
    except Exception as e:
        print(f"❌ CRITICAL: Could not connect to @{TARGET_USERNAME} - {e}")

    print(f"🔥 Dark Devil is Live! Powered by @XLDAREDEVIL")
    await idle()
    await app.stop()

if __name__ == "__main__":
    # Start Flask Server
    keep_alive()
    # Start Bot
    app.run(start_bot())