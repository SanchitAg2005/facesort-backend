from db.supabase import delete
from utils.files import clear_tmp_dir
from utils.logger import log


def cleanup_job(job):
    # Cleanup only after delivery
    if not job.get("delivered_at"):
        return

    # 1. Delete uploaded job images from Supabase
    for path in job.get("image_paths", []):
        try:
            delete(path)
        except Exception:
            pass

    # 2. Clear worker temp directory
    clear_tmp_dir()

    log(f"Cleanup completed for job {job['_id']}")
