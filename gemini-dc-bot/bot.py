import os

import discord
from dotenv import load_dotenv


import model
import attachments
from logger import logger

load_dotenv("../.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user.name} (ID: {client.user.id})")
    print("-" * 32)


@client.event
async def on_message(message):
    author = message.author
    channel = message.channel
    content = message.content
    if author == client.user:
        return
    if not client.user.mentioned_in(message):
        return
    logger.info(f"From {author} in channel {channel}\n\t{content}")

    user_message = [content]
    if message.attachments:
        images = attachments.get_images(message.attachments)
        user_message.extend(images)
        logger.info(f"with {len(images)} image(s)")

    response = model.send_message(user_message)
    await message.channel.send(response)


TOKEN = os.getenv("BOT_TOKEN")
client.run(TOKEN)
