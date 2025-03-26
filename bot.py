# @Safaridev
import os
import logging
import asyncio
import pytesseract
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image
import os
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO)

API_ID = int(os.getenv("API_ID", "15561124"))
API_HASH = os.getenv("API_HASH", "277b0bfae263554a5211e856d389b9d8") 
BOT_TOKEN = os.getenv("BOT_TOKEN", "7140468132:AAF302Ux7AqKEr5yHVl0CLre6MfEIXUMB0Q")

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "running"}

async def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "कोई टेक्स्ट नहीं मिला।"
    except Exception as e:
        return f"त्रुटि हुई: {str(e)}"

@bot.on_message(filters.photo)
async def handle_photo(client, message: Message):
    file_path = await message.download()
    extracted_text = await extract_text_from_image(file_path)
    os.remove(file_path)  
    await message.reply_text(f"📜 **निकाला गया टेक्स्ट:**\n\n```{extracted_text}```", parse_mode="markdown")

@bot.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text("👋 नमस्ते! मैं एक OCR बॉट हूँ। कोई भी फोटो भेजो, और मैं उसमें से टेक्स्ट निकालकर वापस भेज दूँगा।")

async def main():
    await bot.start()
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    asyncio.run(main())
