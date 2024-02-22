from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 1
api_hash = ""
phone = ""

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
    all_messages.extend(message.message for message in messages)
    offset_id = messages[-1].id

print("Saving data to file...")
with open("messages.csv", "w", encoding="UTF-8") as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(["message"])
    writer.writerows([[message] for message in all_messages])

print('Parsing messages from the chat was successful')
