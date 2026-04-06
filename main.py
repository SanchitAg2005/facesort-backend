import time
from db.service_status import heartbeat
from stages.friends import process_friends
from stages.jobs import process_jobs
from config import SLEEP_SECONDS

print("🚀 FaceSort Worker 2.0 running")

while True:
    try:
        heartbeat()
        process_friends()
        process_jobs()
    except Exception as e:
        print("Worker error:", e)

    time.sleep(SLEEP_SECONDS)
