import numpy as np

STRICT = 0.40
LOOSE = 0.46


def match(scanned, known_people):
    results = {p["friend_id"]: [] for p in known_people}


    scan_enc = np.array([f["encoding"] for f in scanned], dtype=np.float32)
    scan_paths = [f["path"] for f in scanned]
    scan_norms = np.linalg.norm(scan_enc, axis=1)

    for i in range(len(scan_enc)):
        best_friend_id = None
        best_dist = float("inf")

        for person in known_people:
            sim = (scan_enc[i] @ person["encodings"].T) / (
                scan_norms[i] * person["norms"]
            )
            dist = 1 - sim
            d = np.min(dist)

            if d < best_dist:
                best_dist = d
                best_friend_id = person["friend_id"]

        if best_dist <= LOOSE:
            results[best_friend_id].append(scan_paths[i])

    return results
