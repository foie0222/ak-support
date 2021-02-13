from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
NETKEIBA_LOGIN_ID = os.getenv('NETKEIBA_LOGIN_ID')
NETKEIBA_LOGIN_PASSWORD = os.getenv('NETKEIBA_LOGIN_PASSWORD')
