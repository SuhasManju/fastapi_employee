import os
import dotenv
dotenv.load_dotenv()
print(os.getenv("DB_USER"))