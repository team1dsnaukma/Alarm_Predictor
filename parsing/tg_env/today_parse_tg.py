from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
import csv
from datetime import datetime, timedelta
import pytz
import os
from preprocessing_tg import preprocess_message

api_id = 123
api_hash = "-"
phone = "+-"

client = TelegramClient(phone, api_id, api_hash)

client.start()

chats = []
last_date = None
chunk_size = 200
groups = []
result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

print("Select a chat for parsing messages:")
for i, chat in enumerate(chats):
    print(f"{i}: {chat.title}")

chat_index = int(input("Enter the chat index: "))
target_chat = chats[chat_index]

today_date = datetime.now(pytz.timezone('Europe/Kiev')).date()
start_date = datetime(today_date.year, today_date.month, today_date.day, 0, 0, 0, tzinfo=pytz.timezone('Europe/Kiev'))
end_date = datetime(today_date.year, today_date.month, today_date.day, 23, 59, 59, tzinfo=pytz.timezone('Europe/Kiev'))

all_messages = []

offset_id = 0
limit = 100

while True:
    history = client(GetHistoryRequest(
        peer=target_chat,
        offset_id=offset_id,
        offset_date=end_date.astimezone(pytz.utc).timestamp(),  # Fetch messages before this timestamp
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))
    if not history.messages:
        break
    messages = history.messages
    all_messages.extend(messages)
    offset_id = messages[-1].id

filtered_messages = [(message.date.astimezone(pytz.timezone('Europe/Kiev')).strftime('%H:%M:%S'),
                      message.date.astimezone(pytz.timezone('Europe/Kiev')).strftime('%Y-%m-%d'),
                      preprocess_message(message.message)) for message in all_messages if start_date <= message.date.astimezone(pytz.timezone('Europe/Kiev')) <= end_date]

folder_path = "/.../Alarm_Predictor/clean_data"
file_path = os.path.join(folder_path, "tg_messages_today.csv")

# Ensure the directory exists, create if not
os.makedirs(folder_path, exist_ok=True)

with open(file_path, "w", encoding="UTF-8") as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(["time", "date", "message"])
    writer.writerows(filtered_messages)

print(f"Messages saved to: {file_path}")

