from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 123
api_hash = "-"
phone = "-"

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

all_messages = []

offset_id = 0
limit = 100

while True:
    history = client(GetHistoryRequest(
        peer=target_chat,
        offset_id=offset_id,
        offset_date=None,
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

with open("messages_.csv", "w", encoding="UTF-8") as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(["time","date","message"])
    for message in all_messages:
        date = message.date.strftime('%Y-%m-%d')
        time = message.date.strftime('%H:%M:%S')
        writer.writerow([time, date, message.message])

