from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv('TINKOFF_TOKEN')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
