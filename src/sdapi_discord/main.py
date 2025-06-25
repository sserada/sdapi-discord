import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


def main():
    client = MyClient()
    # ここにBotのトークンを設定しますが、次のIssueで.envから読み込むように変更します
    # client.run('YOUR_DISCORD_BOT_TOKEN')

if __name__ == '__main__':
    main()
