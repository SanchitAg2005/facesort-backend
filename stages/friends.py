from db.mongo import get_queued_friends, mark_friend_processed
from db.supabase import download, upload, delete
from ml.encode import encode_friend

import cv2
import numpy as np


def process_friends():
    for friend in get_queued_friends():
        # 1. Download original image
        img_bytes = download(friend["original_image_path"])

        # 2. Generate embedding pickle (pre-CUDA logic)
        emb_pickle = encode_friend(img_bytes, friend["name"])
        emb_path = friend["original_image_path"].replace(
            "original.jpg", "embedding.pkl"
        )
        upload(emb_path, emb_pickle)

        # 3. Create thumbnail
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise RuntimeError("Failed to decode image for thumbnail")

        thumb = cv2.resize(img, (200, 200))
        ok, thumb_buf = cv2.imencode(".jpg", thumb)
        if not ok:
            raise RuntimeError("Failed to encode thumbnail")

        thumb_path = friend["original_image_path"].replace(
            "original.jpg", "thumb.jpg"
        )
        upload(thumb_path, thumb_buf.tobytes(), content_type="image/jpeg")

        # 4. Delete original image from Supabase
        delete(friend["original_image_path"])

        # 5. Update MongoDB
        mark_friend_processed(friend["_id"], {
            "embedding_path": emb_path,
            "thumbnail_path": thumb_path
        })
