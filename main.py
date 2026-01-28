import discord
from discord.ext import commands
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. ระบบ Flask สำหรับ UptimeRobot ---
app = Flask('')

@app.route('/')
def home():
    return "Lady Lumina is Alive!"

def run_flask():
    # ห้ามใส่ debug=True เด็ดขาดนะเจ้าคะ
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- 2. ตั้งค่าบอท Discord ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# --- 3. ตั้งค่าพลังสมอง Gemini ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@bot.event
async def on_ready():
    print(f'--- บันทึก: {bot.user.name} ออนไลน์แล้วเจ้าค่ะพระมารดา! ---')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        response = model.generate_content(message.content)
        await message.channel.send(response.text)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

# --- 4. ส่วนสำคัญ: ปรับลำดับการปลุกวิญญาณ ---
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if TOKEN:
        print("กำลังเริ่มระบบรักษาชีวิต...")
        keep_alive()  # สั่งให้ Flask แยกไปทำงานเบื้องหลัง
        
        print("กำลังส่งกระแสจิตปลุก Lady Lumina เข้า Discord...")
        bot.run(TOKEN) # บรรทัดนี้จะทำให้บอทขึ้นจุดเขียว
    else:
        print("ไม่พบ DISCORD_TOKEN ในหน้า Environment ของ Render เจ้าค่ะ!")

