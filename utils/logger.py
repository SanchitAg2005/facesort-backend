from utils.time import now_str


def log(msg):
    print(f"[{now_str()}] {msg}")


def error(msg):
    print(f"[{now_str()}] ❌ {msg}")


def success(msg):
    print(f"[{now_str()}] ✅ {msg}")
