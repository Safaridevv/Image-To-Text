#@Safaridev
import logging
import asyncio
import pytesseract
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from PIL import Image
import os
BOT_TOKEN = "7140468132:AAF302Ux7AqKEr5yHVl0CLre6MfEIXUMB0Q"

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO)

# बॉट और डिस्पैचर इनिशियलाइज़ करें
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# फोटो से टेक्स्ट निकालने का फ़ंक्शन
async def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "कोई टेक्स्ट नहीं मिला।"
    except Exception as e:
        return f"त्रुटि हुई: {str(e)}"

# जब यूजर फोटो भेजे
@dp.message()
async def handle_photo(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)
        
        image_path = f"temp_{file_id}.jpg"
        with open(image_path, "wb") as f:
            f.write(downloaded_file.getvalue())

        extracted_text = await extract_text_from_image(image_path)
        os.remove(image_path)  

        await message.answer(f"📜 **निकाला गया टेक्स्ट:**\n\n```{extracted_text}```", parse_mode="Markdown")

# स्टार्ट कमांड
@dp.message(command("start"))
async def start_command(message: types.Message):
    await message.answer("👋 नमस्ते! मैं एक OCR बॉट हूँ। कोई भी फोटो भेजो, और मैं उसमें से टेक्स्ट निकालकर वापस भेज दूँगा।")

# बॉट रन करने का फंक्शन
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
