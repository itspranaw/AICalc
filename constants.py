from dotenv import load_dotenv
import os
load_dotenv()

SERVER_URL = 'localhost'
PORT = '8900'
ENV = 'dev'

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb+srv://pranawkk0:Pass%401223@<cluster-url>/test')
DB_NAME = os.getenv('DB_NAME', 'calculator_db')
