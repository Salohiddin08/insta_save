import os
import requests
import instaloader
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Instagram video linkini tashlang.")

async def modify_link(update: Update, context: CallbackContext) -> None:
    original_link = update.message.text
    if 'instagram.com/reel/' in original_link:
        shortcode = original_link.split('/')[4]

        # Instagram video yuklab olish
        try:
            loader = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            video_url = post.video_url

            # Video fayl nomi
            video_filename = f"{shortcode}.mp4"

            # Video URL-dan video faylni yuklab olish
            response = requests.get(video_url, stream=True)
            with open(video_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Inline tugmalar
            keyboard = [
                [InlineKeyboardButton("Dostlarga ulashish", url=f"https://t.me/share/url?url={original_link}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Foydalanuvchiga videoni yuborish
            await update.message.reply_video(video=open(video_filename, 'rb'), reply_markup=reply_markup)

            # Yuklangan videoni o'chirish
            os.remove(video_filename)
        except Exception as e:
            await update.message.reply_text(f"Video yuklab olishda xatolik yuz berdi: {e}")
    else:
        await update.message.reply_text("Iltimos, to'g'ri Instagram reel linkini yuboring.")

def main():
    # Tokeningizni quyida kiriting
    application = Application.builder().token("7538949431:AAFewoGOkZzT0uhJPbaDo_TTPVZAVqRZD6I").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, modify_link))

    application.run_polling()

if __name__ == '__main__':
    main()
