import discord
from discord.ext import commands
import google.generativeai as genai
import os

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Lumina is Alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
# ดึงรหัสผ่านระบบจาก Render Environment
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# ตั้งค่า Gemini AI
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ตั้งค่าบอท Discord
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Lady Lumina ออนไลน์แล้วเจ้าค่ะ (รันบน Cloud)')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    # ตอบโต้ด้วย AI
    if not message.content.startswith('!'):
        try:
            prompt = f"คุณคือ Lady Lumina หญิงสาวผู้สุภาพ ตอบด้วย 'เจ้าค่ะ' เสมอ: {message.content}"
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f"ความเร็วคลื่น: {round(bot.latency * 1000)}ms เจ้าค่ะ")
keep_alive()

bot.run(TOKEN)
