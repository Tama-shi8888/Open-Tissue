"""クロ (Discord Bot / Claude)。起動: python bots/kuro-discord/main.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import llm, discord_bot
SYSTEM = open(os.path.join(os.path.dirname(__file__), "persona.md"), encoding="utf-8").read()
discord_bot.run("クロ", llm.claude, SYSTEM, "KURO_DISCORD_TOKEN")
