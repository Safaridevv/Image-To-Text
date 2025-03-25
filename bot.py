import logging
import pytesseract
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from PIL import Image
import os
from config import BOT_TOKEN

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO)

# बॉट और डिस्पैचर इनिशियलाइज़ करें
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# फोटो को प्रोसेस करके टेक्स्ट निकालने का फ़ंक्शन
async def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "कोई टेक्स्ट नहीं मिला।"
    except Exception as e:
        return f"त्रुटि हुई: {str(e)}"

# जब यूजर फोटो भेजे
@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id  # सबसे बड़ी क्वालिटी की इमेज लें
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)
    
    image_path = f"temp_{file_id}.jpg"
    with open(image_path, "wb") as f:
        f.write(downloaded_file.getvalue())

    extracted_text = await extract_text_from_image(image_path)
    os.remove(image_path)  # टेम्प फाइल डिलीट करें
    
    await message.reply(f"📜 **निकाला गया टेक्स्ट:**\n\n```{extracted_text}```", parse_mode="Markdown")

# स्टार्ट कमांड
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("👋 नमस्ते! मैं एक OCR बॉट हूँ। बस कोई भी फोटो भेजो, और मैं उसमें से टेक्स्ट निकालकर वापस भेज दूँगा।")

# बॉट रन करें
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
