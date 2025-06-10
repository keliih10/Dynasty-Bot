import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Setup Flask to keep alive (optional, not required on Railway)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Track ready users
ready_users = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().strip() == "ready":
        if message.author.id not in ready_users:
            ready_users[message.author.id] = message.author.display_name
            await message.channel.send(f"{message.author.display_name} is ready!")

        if len(ready_users) == 6:
            await message.channel.send("Week has advanced!")
            ready_users.clear()

    await bot.process_commands(message)

@bot.command()
async def readylist(ctx):
    if not ready_users:
        await ctx.send("No one has typed 'Ready' yet.")
    else:
        names = "\n".join(f"• {name}" for name in ready_users.values())
        await ctx.send(f"Users who typed 'Ready':\n{names}")

# Run everything
keep_alive()
bot.run(os.getenv("TOKEN"))
