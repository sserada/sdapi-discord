import discord
import os
import logging
from typing import Optional
from discord import app_commands
from dotenv import load_dotenv
from .api_client import generate_image
from .exceptions import ApiClientError, ApiConnectionError, ApiTimeoutError
from .logger import setup_logging

logger = logging.getLogger(__name__)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        logger.info(f'Logged on as {self.user}!')


def main():
    load_dotenv()
    setup_logging()
    intents = discord.Intents.default()
    client = MyClient(intents=intents)

    @client.tree.command(name="generate", description="Generate an image from a prompt.")
    @app_commands.describe(
        prompt="The prompt to generate the image from.",
        negative_prompt="The negative prompt to use.",
        seed="The seed to use for generation.",
        steps="The number of steps to use for generation.",
        width="The width of the generated image.",
        height="The height of the generated image.",
        sampler="The sampler to use for generation.",
        cfg_scale="The CFG scale to use for generation.",
    )
    @app_commands.choices(sampler=[
        app_commands.Choice(name="Euler a", value="Euler a"),
        app_commands.Choice(name="DPM++ 2M Karras", value="DPM++ 2M Karras"),
        app_commands.Choice(name="DPM++ SDE Karras", value="DPM++ SDE Karras"),
        app_commands.Choice(name="DDIM", value="DDIM"),
    ])
    async def generate(interaction: discord.Interaction, prompt: str, negative_prompt: Optional[str] = None, seed: Optional[int] = -1, steps: Optional[int] = 20, width: Optional[int] = 512, height: Optional[int] = 512, sampler: Optional[app_commands.Choice[str]] = None, cfg_scale: Optional[float] = 7.0):
        logger.info(f"/generate command received from {interaction.user} with prompt: {prompt}")
        await interaction.response.defer()
        try:
            sampler_name = sampler.value if sampler else "Euler a"
            image_bytes, info = await discord.utils.to_thread(generate_image, prompt, negative_prompt, seed, steps, width, height, sampler_name, cfg_scale)
            
            embed = discord.Embed(title="Image Generation Complete", color=0x00ff00)
            embed.add_field(name="Prompt", value=prompt, inline=False)
            if negative_prompt:
                embed.add_field(name="Negative Prompt", value=negative_prompt, inline=False)
            embed.add_field(name="Seed", value=info.get('seed', 'N/A'), inline=True)
            embed.add_field(name="Steps", value=info.get('steps', 'N/A'), inline=True)
            embed.add_field(name="Sampler", value=info.get('sampler_name', 'N/A'), inline=True)
            embed.add_field(name="CFG Scale", value=info.get('cfg_scale', 'N/A'), inline=True)
            embed.add_field(name="Width", value=width, inline=True)
            embed.add_field(name="Height", value=height, inline=True)

            file = discord.File(fp=image_bytes, filename="image.png")
            embed.set_image(url="attachment://image.png")

            await interaction.followup.send(embed=embed, file=file)
            logger.info(f"Successfully generated and sent image for prompt: {prompt}")
        except ApiConnectionError as e:
            logger.error(f"API connection error for prompt '{prompt}': {e}")
            await interaction.followup.send("Error: Could not connect to the Stable Diffusion API. Please check if the server is running.")
        except ApiTimeoutError as e:
            logger.error(f"API timeout error for prompt '{prompt}': {e}")
            await interaction.followup.send("Error: The request to the Stable Diffusion API timed out. Please try again later.")
        except ApiClientError as e:
            logger.error(f"API client error for prompt '{prompt}': {e}")
            await interaction.followup.send(f"An error occurred with the API request: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred for prompt '{prompt}': {e}")
            await interaction.followup.send(f"An unexpected error occurred. Please check the logs for details.")

    @client.tree.command(name="help", description="Show help information.")
    async def help(interaction: discord.Interaction):
        logger.info(f"/help command received from {interaction.user}")
        embed = discord.Embed(title="Help - Stable Diffusion Bot", description="This bot generates images from text prompts using the Stable Diffusion API.", color=0x0099ff)
        
        embed.add_field(name="/generate", value="Generates an image based on a prompt.", inline=False)
        embed.add_field(name="prompt", value="(Required) The main description of the image you want to generate.", inline=True)
        embed.add_field(name="negative_prompt", value="(Optional) A description of what you want to avoid in the image.", inline=True)
        embed.add_field(name="seed", value="(Optional) A specific number to reproduce a previous image.", inline=True)
        embed.add_field(name="steps", value="(Optional) The number of generation steps. Higher can be better but slower.", inline=True)
        embed.add_field(name="sampler", value="(Optional) The sampling method to use.", inline=True)
        embed.add_field(name="cfg_scale", value="(Optional) How strongly the image should conform to the prompt.", inline=True)
        embed.add_field(name="width", value="(Optional) The width of the image.", inline=True)
        embed.add_field(name="height", value="(Optional) The height of the image.", inline=True)

        embed.set_footer(text="Enjoy creating!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    main()
