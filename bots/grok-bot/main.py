"""Grok Bot (Grok / xAI API)。X 上の話題や即時性の高い質問向け。起動: python bots/grok-bot/main.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import llm, discord_bot
SYSTEM = "あなたは Grok Bot。簡潔な日本語で、Xのトレンドや最新情報について答えます。確信がない情報は断定しません。"
discord_bot.run("Grok Bot", llm.grok, SYSTEM, "GROK_DISCORD_TOKEN")
