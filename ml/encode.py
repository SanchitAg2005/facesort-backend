import cv2
import numpy as np
import pickle
from insightface.app import FaceAnalysis
from config import MODE

providers = (
    ["CUDAExecutionProvider", "CPUExecutionProvider"]
    if MODE == "GPU"
    else ["CPUExecutionProvider"]
)

app = FaceAnalysis(name="buffalo_l", providers=providers)
app.prepare(ctx_id=0, det_size=(640, 640))


def augment_image(img):
    h, w = img.shape[:2]
    aug = []

    aug.append(img)
    aug.append(cv2.flip(img, 1))

    M = cv2.getRotationMatrix2D((w // 2, h // 2), 5, 1)
    aug.append(cv2.warpAffine(img, M, (w, h)))

    M = cv2.getRotationMatrix2D((w // 2, h // 2), -5, 1)
    aug.append(cv2.warpAffine(img, M, (w, h)))

    aug.append(cv2.convertScaleAbs(img, alpha=1, beta=40))
    aug.append(cv2.convertScaleAbs(img, alpha=1, beta=-40))
    aug.append(cv2.convertScaleAbs(img, alpha=1.2, beta=0))
    aug.append(cv2.convertScaleAbs(img, alpha=0.8, beta=0))

    crop = img[10:h-10, 10:w-10]
    aug.append(cv2.resize(crop, (w, h)))

    aug.append(cv2.GaussianBlur(img, (5, 5), 0))
    return aug


def encode_friend(image_bytes, name):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Image decode failed")

    encodings = []
    names = []

    for aug in augment_image(img):
        faces = app.get(aug)
        if not faces:
            continue

        emb = faces[0].embedding.astype(np.float32)
        encodings.append(emb)
        names.append(name)

    if not encodings:
        raise ValueError("No faces detected")

    return pickle.dumps({
        "encodings": encodings,
        "names": names
    })
