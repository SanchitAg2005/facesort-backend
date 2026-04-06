import os
import shutil

TMP_DIR = os.path.join(os.getcwd(), "tmp")


def ensure_tmp_dir():
    os.makedirs(TMP_DIR, exist_ok=True)


def clear_tmp_dir():
    if not os.path.isdir(TMP_DIR):
        return

    for name in os.listdir(TMP_DIR):
        path = os.path.join(TMP_DIR, name)
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception:
            pass
