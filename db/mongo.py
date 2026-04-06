from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from config import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

friends_col = db.friends
jobs_col = db.jobs
service_col = db.service_status


def get_queued_friends():
    return list(friends_col.find({"status": "queued"}))


def mark_friend_processed(friend_id, data):
    data["status"] = "processed"
    data["updated_at"] = datetime.utcnow()
    friends_col.update_one({"_id": friend_id}, {"$set": data})


def lock_pending_job():
    return jobs_col.find_one_and_update(
        {"status": "queued"},
        {"$set": {"status": "processing", "in_progress": datetime.utcnow()}},
        return_document=ReturnDocument.AFTER
    )


def complete_job(job_id, result, total_faces):
    jobs_col.update_one(
        {"_id": job_id},
        {"$set": {
            "status": "completed",
            "result": result,
            "total_faces_detected": total_faces,
            "delivered_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }}
    )
