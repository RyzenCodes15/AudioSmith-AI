import requests
import time
import os

BASE_URL = "http://backend:8000/api/v1"
TEST_USER = {"email": f"test_{int(time.time())}@example.com", "password": "password123", "full_name": "Test User"}

print("Registering user...")
requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
print("Logging in...")
res = requests.post(f"{BASE_URL}/auth/login", json={"email": TEST_USER["email"], "password": TEST_USER["password"]})
token = res.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

def process_file(filename):
    print(f"\nProcessing {filename}...")
    filepath = f"/tmp/test_audio/{filename}"
    with open(filepath, "rb") as f:
        files = {"file": (filename, f, "audio/" + filename.split(".")[-1])}
        res = requests.post(f"{BASE_URL}/uploads/upload", headers=headers, files=files)
    
    if res.status_code != 201:
        print("Upload failed:", res.text)
        return
        
    audio_id = res.json()["id"]
    print(f"Uploaded successfully. Audio ID: {audio_id}")
    
    start_time = time.time()
    while True:
        res = requests.get(f"{BASE_URL}/uploads/{audio_id}", headers=headers)
        data = res.json()
        status = data["status"]
        if status == "completed":
            print(f"[{filename}] Inference complete in {time.time() - start_time:.2f}s!")
            print(f"[{filename}] Enhanced file ID: {data['enhanced_file_id']}")
            break
        elif status == "failed":
            print(f"[{filename}] Processing failed!")
            break
        time.sleep(1)

process_file("test.wav")
process_file("test.mp3")
process_file("test.flac")
