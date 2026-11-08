"""Discord Bot 共通実装。メンション or DM に LLM で返信する。"""
import asyncio, os, sys, discord
sys.path.insert(0, os.path.dirname(__file__))

def run(name, ask, system, token_env):
    intents = discord.Intents.default(); intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{name} ready as {client.user}")

    @client.event
    async def on_message(m):
        if m.author.bot or not (client.user in m.mentions or isinstance(m.channel, discord.DMChannel)):
            return
        text = m.clean_content.replace(f"@{client.user.name}", "").strip()
        async with m.channel.typing():
            reply = await asyncio.to_thread(ask, [{"role": "user", "content": text}], system)
        for i in range(0, len(reply), 1900):
            await m.reply(reply[i:i + 1900])

    client.run(os.environ[token_env])
