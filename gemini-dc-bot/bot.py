import os

import discord
from dotenv import load_dotenv

load_dotenv("../.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} (ID: {client.user.id})")
    print("-" * 32)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not client.user.mentioned_in(message):
        return
    await message.channel.send(f"Hello, world!")


TOKEN = os.getenv("BOT_TOKEN")
client.run(TOKEN)
