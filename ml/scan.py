import cv2
import numpy as np
from insightface.app import FaceAnalysis
from config import MODE

providers = (
    ["CUDAExecutionProvider", "CPUExecutionProvider"]
    if MODE == "GPU"
    else ["CPUExecutionProvider"]
)

app = FaceAnalysis(name="buffalo_l", providers=providers)
app.prepare(ctx_id=0, det_size=(640, 640))


def scan_image(image_bytes, path):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return []

    faces = app.get(img)
    scanned = []

    for f in faces:
        scanned.append({
            "encoding": f.embedding.astype(np.float32),
            "path": path
        })

    return scanned
