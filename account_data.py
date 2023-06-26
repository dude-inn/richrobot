"""
Модуль для загрузки токенов, аккаунтов.
"""

from dotenv import load_dotenv
import os


load_dotenv()

TINKOFF_TOKEN = os.getenv('TINKOFF_TOKEN')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')