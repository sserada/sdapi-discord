import discord
import os
from dotenv import load_dotenv
from .api_client import async_generate_image

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')


def main():
    load_dotenv()
    intents = discord.Intents.default()
    client = MyClient(intents=intents)

    @client.tree.command(name="generate", description="Generate an image from a prompt.")
    async def generate(interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            image_bytes = await discord.utils.to_thread(async_generate_image, prompt)
            file = discord.File(fp=image_bytes, filename="image.png")
            await interaction.followup.send(f"Prompt: {prompt}", file=file)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    main()
