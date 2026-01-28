import discord
from discord.ext import commands
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. ระบบรักษาชีวิต (Flask) ---
app = Flask('')

@app.route('/')
def home():
    return "Lumina is Awake!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. ตั้งค่าบอท Discord ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# --- 3. ตั้งค่าพลังสมอง Gemini ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print("--- Lady Lumina is Online Now! ---")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        # รับคำถามจาก Discord ส่งให้ Gemini
        response = model.generate_content(message.content)
        await message.channel.send(response.text)
    except Exception as e:
        print(f"Error: {e}")

# --- 4. ส่วนสั่งรันระบบ ---
if __name__ == "__main__":
    # ดึงกุญแจจาก Environment Variables ใน Render
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if TOKEN:
        keep_alive()   # สั่งรันเว็บเบื้องหลัง
        bot.run(TOKEN) # สั่งรันบอทเข้า Discord
    else:
        print("Error: No DISCORD_TOKEN found!")
