import discord
import datetime

TOKEN = 'Bot Token'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def convert_link(original_url):
    if original_url.startswith("https://x.com/") or original_url.startswith("https://twitter.com/"):
        return original_url.replace("https://x.com/", "https://fxtwitter.com/").replace("https://twitter.com/", "https://fxtwitter.com/")
    return original_url

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith(";delete"):
            if message.reference:
                referenced_message = await message.channel.fetch_message(message.reference.message_id)
                if referenced_message.author == client.user:
                    await referenced_message.edit(content="Deleted Message.")
                    await message.add_reaction("✅")
                else:
                    await message.channel.send("This message is not a converted message.")
            else:
                await message.channel.send("Please send a reply.")
        else:
            original_urls = [word for word in message.content.split() if word.startswith(("https://x.com/", "https://twitter.com/"))]
            if original_urls:
                for original_url in original_urls:
                    converted_url = convert_link(original_url)
                    log_conversion(message.author.id, original_url, converted_url)
                    msg = await message.channel.send(converted_url)

client.run(TOKEN)
