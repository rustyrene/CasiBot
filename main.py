from dotenv import load_dotenv
import os
import discord

if __name__ == "__main__":
    # Load the token from your .env file
    load_dotenv()
    token = os.getenv("TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is online!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content.startswith("-ping"):
            await message.channel.send("Pong!")

    client.run(token=token)