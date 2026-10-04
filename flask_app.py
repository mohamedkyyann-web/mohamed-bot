import os, requests, random, asyncio, sqlite3
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from PIL import Image, ImageDraw

BOT_TOKEN = "8865686478:AAG2-yLWMipxR9fMH0h1fep42bAhTBYiB-w"
PORT = int(os.environ.get("PORT", 8080))

flask_app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

def get_kb():
    return ReplyKeyboardMarkup([["🧠 اسألني","🎨 ارسم لي"],["🔳 سوي QR","✨ اسمي ذهبي"]],resize_keyboard=True)

async def start(update, context):
    await update.message.reply_text(f"هلا يا {update.effective_user.first_name}! 🚀 V123 صاروخ على Railway!", reply_markup=get_kb())

async def msg_h(update, context):
    t=(update.message.text or "").strip()
    if "ذهبي" in t or "ذهب" in t:
        W,H=1024,1024; img=Image.new('RGB',(W,H),(10,10,10)); d=ImageDraw.Draw(img)
        d.text((W//2,H//2),update.effective_user.first_name[:12],fill=(255,215,0),anchor="mm")
        fp=f"/tmp/{random.randint(1,9999999)}.jpg"; img.save(fp); await update.message.reply_photo(open(fp,"rb"),reply_markup=get_kb()); os.remove(fp); return
    await update.message.reply_text(f"سؤالك: {t}\nالبوت شغال على Railway الآن! 🔥", reply_markup=get_kb())

telegram_app.add_handler(CommandHandler("start",start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,msg_h))

@flask_app.route(f"/{BOT_TOKEN}",methods=["POST"])
def webhook():
    data=request.get_json(force=True); upd=Update.de_json(data,telegram_app.bot)
    async def run():
        await telegram_app.initialize(); await telegram_app.process_update(upd); await telegram_app.shutdown()
    asyncio.run(run()); return "ok"

@flask_app.route("/")
def home(): return "V123 Railway OK"

@flask_app.route("/setwebhook")
def setwh():
    domain=os.environ.get("RAILWAY_PUBLIC_DOMAIN","")
    if domain:
        r=requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url=https://{domain}/{BOT_TOKEN}")
        return r.text
    return "no domain"

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=PORT)
