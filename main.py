from dotenv import load_dotenv
import os
import discord
from games import roulette
from database import update_balance, create_user, get_balance

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

        if message.content.startswith("-reg"):
            try:
                await create_user(message.author)
                await message.channel.send("Your account was created succesfully. You start with 5000 Coins")
            except Exception:
                await message.channel.send("There was a problem creating your account. You might already be registered")

        if message.content.startswith("-balance"):
            try:
                balance = await get_balance(message.author)
                await message.channel.send(f"You currently habe {balance} coins")
            except Exception as e:
                print(e)
                await message.channel.send("Sorry, but you dont have an account yet. User -reg to register")

        if message.content.startswith("-roulette"):
            args = message.content.split(" ")[1:]
            prize = roulette.play(args)
            await message.channel.send(f"The color is: {prize[1]}!")
            if prize[0] > 0:
                await message.channel.send(f"Congratulations, you have won: {prize[0]} coins!")
            else:
                await message.channel.send(f"You have lost {prize[0]} coins!")
            await update_balance(message.author, prize[0])

    client.run(token=token)