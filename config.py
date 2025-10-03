import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://niraj22311707_db_user:KLBxjmbWuEhPmmi9@cluster0.o57o7b7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
DB_NAME = "mydb"