# Bots
- `kuro-discord/` クロ (Claude / Discord)。`ANTHROPIC_API_KEY`, `KURO_DISCORD_TOKEN`
- `grok-bot/` Grok Bot (xAI / Discord)。`XAI_API_KEY`, `GROK_DISCORD_TOKEN`

```
pip install -r bots/requirements.txt
python bots/kuro-discord/main.py
```
Discord Developer Portal で Bot を作成し、Message Content Intent を有効化してください。常駐は systemd / Docker 等で行います。
