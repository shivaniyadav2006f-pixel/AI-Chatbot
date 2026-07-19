from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_SECRET_KEY = os.getenv("UNSPLASH_SECRET_KEY")

print("Access Key:", UNSPLASH_ACCESS_KEY)
print("Secret Key:", UNSPLASH_SECRET_KEY)