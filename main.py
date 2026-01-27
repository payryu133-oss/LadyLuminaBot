import discord
from discord.ext import commands
import google.generativeai as genai
import os

# ดึงรหัสจาก Environment Variables (เดี๋ยวไปใส่ในหน้าเว็บ Koyeb)
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} พร้อมรับใช้แล้วเจ้าค่ะ!')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    prompt = f"คุณคือ Lady Lumina ผู้สูงศักดิ์ ตอบสุภาพ: {message.content}"
    try:
        response = ai_model.generate_content(prompt)
        await message.channel.send(response.text)
    except:
        await message.channel.send("กระแสน้ำแปรปรวนนิดหน่อยเจ้าค่ะ...")

bot.run(TOKEN)
