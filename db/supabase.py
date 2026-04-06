import requests
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_BUCKET

HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
}


def download(path):
    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{path}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.content


def upload(path, data, content_type="application/octet-stream"):
    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{path}"
    r = requests.post(
        url,
        headers={**HEADERS, "Content-Type": content_type},
        data=data
    )
    r.raise_for_status()


def delete(path):
    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{path}"
    r = requests.delete(url, headers=HEADERS)
    r.raise_for_status()
