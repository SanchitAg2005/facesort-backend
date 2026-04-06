import pickle
import numpy as np
from pymongo import MongoClient
from datetime import datetime

from config import MONGO_URI, MONGO_DB
from db.mongo import lock_pending_job, complete_job, jobs_col
from db.supabase import download
from ml.scan import scan_image
from ml.match import match
from stages.delivery import deliver_job
from stages.cleanup import cleanup_job


client = MongoClient(MONGO_URI)
db = client[MONGO_DB]


def process_jobs():
    job = lock_pending_job()
    if not job:
        return

    # SAFETY: job must have selected friends
    if not job.get("selected_friend_ids"):
        jobs_col.update_one(
            {"_id": job["_id"]},
            {"$set": {"status": "failed", "updated_at": datetime.utcnow()}}
        )
        return

    scanned = []

    # 1️⃣ SCAN IMAGES
    for path in job["image_paths"]:
        img = download(path)
        scanned.extend(scan_image(img, path))

    # 2️⃣ LOAD FRIEND EMBEDDINGS
    known_people = []
    for fid in job["selected_friend_ids"]:
        friend = db.friends.find_one({"_id": fid})
        data = pickle.loads(download(friend["embedding_path"]))

        enc = np.array(data["encodings"], dtype=np.float32)
        norms = np.linalg.norm(enc, axis=1)

        known_people.append({
            "friend_id": str(friend["_id"]),
            "name": friend["name"],
            "encodings": enc,
            "norms": norms
        })

    # 3️⃣ MATCH
    result = match(scanned, known_people)

    # 4️⃣ SAVE MATCH RESULT
    jobs_col.update_one(
        {"_id": job["_id"]},
        {"$set": {
            "result": result,
            "total_faces_detected": len(scanned),
            "updated_at": datetime.utcnow()
        }}
    )

    # 🔥 REQUIRED: reload job so `result` exists
    job = jobs_col.find_one({"_id": job["_id"]})

    # 5️⃣ DELIVERY
    deliver_job(job)
    job = jobs_col.find_one({"_id": job["_id"]})
    # 6️⃣ CLEANUP
    cleanup_job(job)

    # 7️⃣ FINALIZE JOB
    complete_job(job["_id"], result, len(scanned))
