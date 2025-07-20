from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me an Amazon or Flipkart product link to get its current price.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        if "amazon" in url:
            title = soup.find(id="productTitle").get_text(strip=True)
            price = soup.find("span", {"class": "a-price-whole"}).get_text(strip=True)
        elif "flipkart" in url:
            title = soup.find("span", {"class": "B_NuCI"}).get_text(strip=True)
            price = soup.find("div", {"class": "_30jeq3"}).get_text(strip=True)
        else:
            await update.message.reply_text("❌ Unsupported URL. Please send a valid Amazon or Flipkart product link.")
            return

        await update.message.reply_text(f"🛒 {title}\n💰 Price: {price}")

    except Exception as e:
        await update.message.reply_text("⚠️ Error fetching price. Try again.")
        print("Error:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot running...")
app.run_polling()