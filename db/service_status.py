from datetime import datetime
from config import MODE
from db.mongo import service_col

WORKER_ID = "facesort-worker-v2"


def heartbeat():
    service_col.update_one(
        {"_id": WORKER_ID},
        {"$set": {
            "status": "online",
            "mode": MODE,
            "last_heartbeat": datetime.utcnow()
        }},
        upsert=True
    )
