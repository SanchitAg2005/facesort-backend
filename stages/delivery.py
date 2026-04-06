from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

from config import MONGO_URI, MONGO_DB
from db.supabase import download
from tg.bot import send_message, send_photo


client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

users_col = db.users
friends_col = db.friends
jobs_col = db.jobs


def deliver_job(job):
    # Idempotency
    if job.get("delivered_at"):
        return

    # Fetch user (ONLY for custom message / username)
    user_id = job.get("user_id")
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    user = users_col.find_one({"_id": user_id})
    if not user:
        raise RuntimeError("User not found for job")

    custom_message = user.get("custom_message")

    if custom_message and custom_message.strip():
        message = custom_message.strip()
    else:
        username = user.get("username", "").strip()
        if username:
            message = (
                "Here's your customized photo album powered by FaceSort ✨\n"
                f"— {username}"
            )
        else:
            message = "Here's your customized photo album powered by FaceSort ✨"

    # 🔥 DELIVERY PER FRIEND
    for friend_id, paths in job["result"].items():
        fid = ObjectId(friend_id)

        friend = friends_col.find_one({"_id": fid})
        if not friend:
            continue

        chat_id = friend.get("telegram_chat_id")
        if not chat_id:
            continue

        # Send message once per friend
        send_message(chat_id, message)

        # Send photos
        for path in paths:
            img_bytes = download(path)
            send_photo(chat_id, img_bytes)

    # Mark delivered
    jobs_col.update_one(
        {"_id": job["_id"]},
        {"$set": {
            "delivered_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }}
    )
