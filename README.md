# sdapi-discord

This project is a Discord bot that uses the Stable Diffusion API to generate images from text prompts.

[日本語のREADMEはこちら](./README-ja.md)

## Features

-   **Image Generation**: Generate images from text prompts using the `/generate` command.
-   **Customizable Parameters**: Adjust various parameters for image generation, such as negative prompts, seed, steps, sampler, and more.
-   **Help Command**: Get information on how to use the bot with the `/help` command.

## Prerequisites

-   Python 3.8 or higher
-   A Discord bot token
-   A running instance of the Stable Diffusion API

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/sdapi-discord.git
    cd sdapi-discord
    ```

2.  **Install dependencies:**

    This project uses [Rye](https://rye-up.com/) for dependency management.

    ```bash
    rye sync
    ```

3.  **Set up environment variables:**

    Create a `.env` file by copying the example file:

    ```bash
    cp .env.example .env
    ```

    Open the `.env` file and add your Discord bot token and the URL of your Stable Diffusion API instance:

    ```
    DISCORD_BOT_TOKEN="your-discord-bot-token"
    SD_API_URL="http://127.0.0.1:7860"
    ```

## Usage

To start the bot, run the following command:

```bash
rye run start
```

### Discord Commands

-   `/generate <prompt> [options]`: Generates an image.
    -   `prompt` (required): The main description of the image you want to generate.
    -   `negative_prompt` (optional): A description of what you want to avoid in the image.
    -   `seed` (optional): A specific number to reproduce a previous image.
    -   `steps` (optional): The number of generation steps.
    -   `sampler` (optional): The sampling method to use.
    -   `cfg_scale` (optional): How strongly the image should conform to the prompt.
    -   `width` (optional): The width of the image.
    -   `height` (optional): The height of the image.
-   `/help`: Shows help information.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.